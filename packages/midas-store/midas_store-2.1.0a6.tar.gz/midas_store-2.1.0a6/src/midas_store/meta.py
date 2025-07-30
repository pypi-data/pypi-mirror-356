META = {
    "type": "time-based",
    "models": {
        "DatabaseCSV": {
            "public": True,
            "any_inputs": True,
            "params": [
                "filename",
                "verbose",
                "path",
                "keep_old_files",
                "unique_filename",
            ],
            "attrs": [],
        },
        "DatabaseHDF5": {
            "public": True,
            "any_inputs": True,
            "params": [
                "filename",
                "verbose",
                "path",
                "keep_old_files",
                "unique_filename",
                "buffer_size",
            ],
            "attrs": [],
        }
    },
}
