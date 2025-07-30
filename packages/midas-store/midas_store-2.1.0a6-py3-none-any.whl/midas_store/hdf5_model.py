import json
import logging
import multiprocessing as mp
import os
import queue
import traceback
from multiprocessing import Queue
from multiprocessing.context import SpawnProcess
from typing import Any, cast
from uuid import uuid4

import numpy as np
import pandas as pd
from midas.util.runtime_config import RuntimeConfig
from mosaik.exceptions import SimulationError

from midas_store.csv_model import serialize

LOG = logging.getLogger(__name__)


class HDF5Model:
    def __init__(
        self,
        filename: str,
        *,
        path: str | None = None,
        unique_filename: bool = False,
        keep_old_files: bool = False,
        buffer_size: int = 1000,
    ):
        if path is None:
            path = RuntimeConfig().paths["output_path"]
            if path is None:
                path = ""
        os.makedirs(path, exist_ok=True)

        self.filename = os.path.abspath(os.path.join(path, filename))

        if self.filename and unique_filename:
            fp, suf = self.filename.rsplit(".", 1)
            self.filename = f"{fp}-{str(uuid4())}.{suf}"
        elif not self.filename:
            self.filename = f"midas-store-results-{str(uuid4())}.hdf5"

        if keep_old_files:
            LOG.debug(
                "Keep_old_files is set to True. Attempting to find a unique "
                "filename for the database."
            )
            incr = 2
            new_filename = self.filename
            while os.path.exists(new_filename):
                fp, suf = self.filename.rsplit(".", 1)
                new_filename = f"{fp}_{incr:03d}.{suf}"
                incr += 1
            self.filename = new_filename
        elif os.path.exists(self.filename):
            os.rename(self.filename, f"{self.filename}.old")

        LOG.info("Saving results to database at '%s'.", self.filename)
        self._buffer_size = buffer_size
        self._buffer_ctr = 0
        self._data = {}
        self._columns = {}
        self._ctx = mp.get_context("spawn")
        self._io_proc: SpawnProcess | None = None
        self._queue: Queue = self._ctx.Queue()
        self._result: Queue = self._ctx.Queue()

    def to_memory(self, sid: str, eid: str, attr: str, val: Any) -> None:
        sid = sid.replace("-", "__")
        key = f"{eid}___{attr}".replace("-", "__")
        if self._columns:
            if sid not in self._columns:
                msg = f"Invalid sid detected: {sid}"
                self._buffer_ctr = 0
                raise ValueError(msg)

            if key not in self._columns[sid]:
                msg = f"Invalid key detected for sid {sid}: {key}"
                self._buffer_ctr = 0
                raise ValueError(msg)

        self._data.setdefault(sid, {})

        self._data[sid].setdefault(key, [])

        if isinstance(val, (list, dict, np.ndarray)):
            val = json.dumps(val)
        elif isinstance(val, pd.DataFrame):
            val = val.to_json()
        else:
            val = serialize(val)
        self._data[sid][key].append(val)

    def step(self):
        if self._io_proc is None:
            LOG.debug("Starting file writer process ...")
            self._io_proc = self._ctx.Process(
                target=run_writer,
                args=(self.filename, self._queue, self._result),
            )

            self._io_proc.start()

            for sid, keys in self._data.items():
                self._columns[sid] = []
                for k in keys:
                    self._columns[sid].append(k)

        if not self._result.empty():
            msg = "Writer process terminated early. Can't continue from here."
            raise SimulationError(msg)

        self._buffer_ctr += 1

        if self._buffer_ctr >= self._buffer_size:
            dfs = {sid: pd.DataFrame(d) for sid, d in self._data.items()}
            self._queue.put(dfs)
            self._data = {}
            self._buffer_ctr = 0

    def finalize(self):
        LOG.info("Shutting down the writer process ...")
        if self._io_proc is None:
            LOG.info("Writer is already None (likely was never initialized).")
        else:
            try:
                if self._buffer_ctr > 0:
                    dfs = {
                        sid: pd.DataFrame(d) for sid, d in self._data.items()
                    }
                    self._queue.put(dfs)
                self._queue.put(-1)
            except ValueError:
                LOG.debug("Queue was already closed.")

            LOG.debug("Waiting for writer to finish ...")
            self._io_proc.join()
            LOG.debug("Writer finished. Check if it left a message ...")

            try:
                msg = self._result.get(timeout=1)
            except queue.Empty:
                LOG.error("Writer finished without message.")
            else:
                log_msg = f"Writer finished with message {msg}"
                if msg.startswith("Error"):
                    LOG.error(log_msg)
                else:
                    LOG.info(log_msg)

        self._result.close()
        self._queue.close()


def run_writer(filename: str, lines: Queue, result: Queue, timeout=300):
    res_msg = "Finished successfully."
    to_ctr = timeout
    append = False
    saved_rows = 0
    new_rows = 0

    try:
        while True:
            try:
                item = lines.get(block=True, timeout=1)
            except queue.Empty:
                to_ctr -= 1
                if to_ctr <= 0:
                    res_msg = (
                        f"Writer received no item in the last {timeout} "
                        "seconds."
                    )
                    break
                continue
            except ValueError:
                res_msg = "Queue was closed. Terminating!"
                break

            if isinstance(item, int):
                LOG.info("Received -1. Terminating!")
                break

            for sid, data in item.items():
                new_rows = data.shape[0]
                data.index += saved_rows
                data.to_hdf(filename, key=sid, format="table", append=append)

            saved_rows += new_rows
            append = True
            to_ctr = timeout
    except Exception:
        res_msg = f"Error writing hdf5: {traceback.format_exc()}"
    except KeyboardInterrupt:
        res_msg = "Interrupted by user!"

    try:
        result.put(res_msg)
    except ValueError:
        LOG.info("Result queue was already closed.")
