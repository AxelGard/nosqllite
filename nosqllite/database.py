import os
import typing
import warnings
from pathlib import Path
from nosqllite import document
from nosqllite import group


class Database(group.Group):
    def __init__(self, file_path:str):
        super().__init__(file_path)

    @staticmethod
    def new(file_path):
        """Make a new database"""
        if os.path.isdir(file_path):
            warnings.warn("there is a dir with that name")
        else:
            os.mkdir(file_path)
        return Database(file_path)

    def __repr__(self) -> str:
        return f"nosqllite.Database({self.file_path})"

