from os import PathLike

import duckdb


class MetadataDB:
    def __init__(self, name="metadata", storage: None | PathLike[str] = None) -> None:
        if storage:
            self.con = duckdb.connect(str(storage))
        else:
            self.con = duckdb.connect()
