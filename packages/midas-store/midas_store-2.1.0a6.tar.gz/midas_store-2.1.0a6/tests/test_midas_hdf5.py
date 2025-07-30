import os
import unittest

import pandas as pd

from midas_store import simulator


class TestMidasHDF5(unittest.TestCase):
    def setUp(self):
        self.inputs1 = {
            "Database-0": {
                "p_mw": {
                    "DummySim-0.DummyHousehold-0": 0.1,
                    "DummySim-0.DummyHousehold-1": 0.2,
                    "DummySim-1.DummyPV-0": 0.3,
                },
                "q_mvar": {
                    "DummySim-0.DummyHousehold-0": 0.01,
                    "DummySim-0.DummyHousehold-1": 0.02,
                    "DummySim-1.DummyPV-0": 0.03,
                },
                "t_air": {"DummyWeather-0.WeatherCurrent-0": 15.0},
                "schedule": {"DummySim-2.DummyCHP-0": [10, 12, 10]},
            }
        }
        self.inputs2 = {
            "Database-0": {
                "p_mw": {
                    "DummySim-0.DummyHousehold-0": 0.02,
                    "DummySim-0.DummyHousehold-1": 0.02,
                    "DummySim-1.DummyPV-0": 0.03,
                    "DummySim-2.DummyCHP-0": 0.5,
                },
                "q_mvar": {
                    "DummySim-0.DummyHousehold-0": 0.01,
                    "DummySim-0.DummyHousehold-1": 0.015,
                    "DummySim-1.DummyPV-0": 0.01,
                },
                "t_air": {"DummyWeather-0.WeatherCurrent-0": 15.0},
                "wind": {"DummyWeather-1.WeatherForecast-0": 20},
            }
        }
        self.i1_cols = {
            "/DummySim__0": [
                "DummyHousehold__0___p_mw",
                "DummyHousehold__1___p_mw",
                "DummyHousehold__0___q_mvar",
                "DummyHousehold__1___q_mvar",
            ],
            "/DummySim__1": ["DummyPV__0___p_mw", "DummyPV__0___q_mvar"],
            "/DummySim__2": ["DummyCHP__0___schedule"],
            "/DummyWeather__0": ["WeatherCurrent__0___t_air"],
        }

    def test_setup(self):
        """Test store creation and ensure to allow only one instance."""
        dbsim = simulator.MidasCSVStore()

        dbsim.init("MidasCSVStore", step_size=900)

        # Only one instance allowed
        with self.assertRaises(ValueError):
            dbsim.create(2, "DatabaseHDF5", filename="there.hdf5")

        dbsim.create(1, "DatabaseHDF5", filename="here.hdf5")

        self.assertIsNotNone(dbsim.database)
        if dbsim.database is not None:
            self.assertIn("here.hdf5", dbsim.database.filename)
        self.assertEqual(900, dbsim.step_size)

        # Only one instance allowed
        with self.assertRaises(ValueError):
            dbsim.create(1, "DatabaseCSV", filename="there.csv")

    def test_step(self):
        dbsim = simulator.MidasCSVStore()
        dbsim.init("MidasCSVStore", step_size=900)
        dbsim.create(1, "DatabaseHDF5", filename="here.hdf5", buffer_size=1)
        dbsim.step(0, self.inputs1)

        with self.assertRaises(ValueError) as context:
            dbsim.step(900, self.inputs2)

        self.assertIn("Invalid key detected", str(context.exception))
        
        with self.assertLogs("midas_store.hdf5_model", level="INFO") as cm:
            dbsim.finalize()
        self.assertIn("Finished successfully", cm.output[-1])

    def test_step_structure_change_within_batch(self):
        dbsim = simulator.MidasCSVStore()
        dbsim.init("MidasCSVStore", step_size=900)
        dbsim.create(1, "DatabaseHDF5", filename="here.hdf5", buffer_size=2)
        dbsim.step(0, self.inputs1)

        with self.assertRaises(ValueError) as context:
            dbsim.step(900, self.inputs2)

        self.assertIn("Invalid key detected", str(context.exception))
        
        with self.assertLogs("midas_store.hdf5_model", level="INFO") as cm:
            dbsim.finalize()
        self.assertIn("Finished successfully", cm.output[-1])

    def test_successful_step(self):
        dbfile = "here.hdf5"
        dbsim = simulator.MidasCSVStore()
        dbsim.init("MidasCSVStore", step_size=900)
        dbsim.create(1, "DatabaseHDF5", filename=dbfile, buffer_size=2)

        for i in range(5):
            dbsim.step(i * 900, self.inputs1)
        dbsim.finalize()

        assert dbsim.database is not None

        tmp = pd.HDFStore(dbsim.database.filename)
        for k in tmp.keys():
            self.assertEqual(len(self.i1_cols[k]), len(tmp[k].columns))
            for c1, c2 in zip(self.i1_cols[k], tmp[k].columns):
                self.assertEqual(str(c1), str(c2))
            self.assertEqual(5, tmp[k].shape[0])
        tmp.close()

    def test_step_no_inputs(self):
        dbfile = "not-there.hdf5"
        dbsim = simulator.MidasCSVStore()
        dbsim.init("MidasCSVStore", step_size=900)
        dbsim.create(1, "DatabaseHDF5", filename=dbfile)
        dbsim.step(0, {})
        dbsim.finalize()
        self.assertFalse(os.path.exists(dbfile))

    def test_huge_dataset(self):
        """Test if a large dataset can be stored. Takes very long
        and should not be necessary most of the time.
        """
        dbsim = simulator.MidasCSVStore()
        dbsim.init("MidasCSVStore", step_size=900)
        dbsim.create(1, "DatabaseHDF5", filename="this_is_huge.hdf5")

        for idx in range(5 * 365 * 24 * 4):
            dbsim.step(idx * 900, self.inputs1)

            if idx % 96 == 0:
                print(idx / 96, end="\r")

        print()
        dbsim.finalize()


if __name__ == "__main__":
    unittest.main()
