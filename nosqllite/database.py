import os
import typing
import warnings
from nosqllite import document


class Database:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        if database_path[-1] != "/":
            database_path += "/"
        self.name = database_path.split("/")[-2]
        self.documents: typing.Dict[str, document.Document] = {}
        self.load(self.database_path)

    @staticmethod
    def new(file_path):
        """Make a new database"""
        if os.path.isdir(file_path):
            warnings.warn("there is a dir with that name")
        else:
            os.mkdir(file_path)
        return Database(file_path)

    def load(self, path: str):
        """Load in all documents in database"""
        files = os.listdir(path)
        if path[-1] != "/":
            path += "/"
        for f in files:
            if ".json" in f:
                name = f.split("/")[-1].split(".json")[0]
                self.documents[name] = document.Document.load(path + f)

    def new_document(self, name: str) -> document.Document:
        """Adds new document to the database"""
        if name in self.documents:
            warnings.warn("tried to make new doc but name taken")
            return self.documents[name]
        new_doc = document.Document(self.database_path + f"/{name}.json")
        self.documents[name] = new_doc
        return self.documents[name]

    def sync(self):
        """Syncs all documents in database"""
        for _, doc in self.documents.items():
            doc.sync()

    def __getitem__(self, key: str):
        return self.documents[key]

    def __setitem__(self, key, value):
        if not isinstance(value, document.Document):
            raise ValueError("set needs to be a nosqllite.Document object")
        self.documents[key] = value

    def __str__(self) -> str:
        return str(self.documents)

    def __repr__(self) -> str:
        return f"nosqllite.Database({self.database_path})"
