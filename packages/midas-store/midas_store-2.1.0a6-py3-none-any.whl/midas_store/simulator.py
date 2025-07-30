import mosaik_api_v3
from midas.util.logging import set_and_init_logger
from mosaik.exceptions import SimulationError
from mosaik_api_v3.types import (
    CreateResult,
    EntityId,
    Meta,
    ModelName,
    OutputData,
    OutputRequest,
    SimId,
    Time,
)
from typing_extensions import override

from . import LOG
from .csv_model import CSVModel
from .hdf5_model import HDF5Model
from .meta import META


class MidasCSVStore(mosaik_api_v3.Simulator):
    """Simulator to store simulation results in a csv file."""

    def __init__(self) -> None:
        super().__init__(META)

        self.sid: SimId | None = None
        self.eid: EntityId = "Database-0"
        self.database: CSVModel | HDF5Model | None = None

        self.filename: str | None = None
        self.step_size: int = 0
        self.current_size: int = 0
        self.saved_rows: int = 0
        self.finalized: bool = False
        self.keep_old_files: bool = True

    @override
    def init(
        self,
        sid: SimId,
        time_resolution: float = 1.0,
        step_size: int = 900,
        **sim_params,
    ) -> Meta:
        self.sid = sid
        self.step_size = step_size

        return self.meta

    @override
    def create(
        self,
        num: int,
        model: ModelName,
        filename: str = "",
        path: str | None = None,
        unique_filename: bool = False,
        keep_old_files: bool = False,
        buffer_size: int = 1000,
        **model_params,
    ) -> list[CreateResult]:
        if num > 1 or self.database is not None:
            errmsg = (
                "You should really not try to instantiate more than one "
                "database. If your need another database, create a new "
                "simulator as well."
            )
            raise ValueError(errmsg)

        if filename and filename.endswith(".hdf5") or model == "DatabaseHDF5":
            self.database = HDF5Model(
                filename,
                path=path,
                unique_filename=unique_filename,
                keep_old_files=keep_old_files,
                buffer_size=buffer_size,
            )
        else:
            self.database = CSVModel(
                filename,
                path=path,
                unique_filename=unique_filename,
                keep_old_files=keep_old_files,
            )

        return [{"eid": self.eid, "type": model}]

    @override
    def step(self, time, inputs, max_advance: Time = 0) -> Time | None:
        if self.database is None:
            msg = "Database is unexpectedly None. Can not proceed any further"
            raise SimulationError(msg)

        data = inputs.get(self.eid, {})

        if not data:
            LOG.info(
                "Did not receive any inputs. "
                "Did you connect anything to the store?"
            )

        for attr, src_ids in data.items():
            for src_id, val in src_ids.items():
                sid, eid = src_id.split(".")
                self.database.to_memory(sid, eid, attr, val)

        self.database.step()

        return time + self.step_size

    @override
    def get_data(self, outputs: OutputRequest) -> OutputData:
        return {}

    @override
    def finalize(self):
        LOG.info("Finalizing database.")
        if self.database is not None:
            self.database.finalize()


if __name__ == "__main__":
    set_and_init_logger(0, "store-logfile", "midas-store.log", replace=True)

    mosaik_api_v3.start_simulation(MidasCSVStore())
