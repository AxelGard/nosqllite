import os
import typing
import json
import datetime
import decimal
import hashlib


def is_json_serializable(value: typing.Any) -> typing.Tuple[bool, str]:
    try:
        json.dumps(value)
        return True, ""
    except (TypeError, OverflowError) as e:
        if isinstance(value, (datetime.datetime, decimal.Decimal)):
            return (
                False,
                f"Value of type {type(value).__name__} needs to be converted to string or number first",
            )
        elif callable(value):
            return False, "Functions cannot be serialized to JSON"
        elif hasattr(value, "__dict__"):
            return (
                False,
                f"Custom object of type {type(value).__name__} cannot be directly serialized",
            )
        else:
            return False, str(e)


class Document:
    def __init__(self, file_path: str) -> None:
        self.name = file_path.split("/")[-1].split(".json")[0]
        self.data: typing.Union[list, dict] = {}
        self.metadata = {}
        self.is_locked = False
        if not Document.is_doc(file_path):
            self.file_path = file_path
            self._write()
        self.metadata, self.data = self._read()
        self.file_path = os.path.abspath(file_path)
        self.has_read = True

    @staticmethod
    def is_doc(file_path) -> bool:
        return os.path.isfile(file_path) and ".json" in file_path

    def sync(self) -> None:
        m, _ = self._read()
        if m["datahash"] == self.hash(self.data):
            return
        else:
            self._write()

    def hash(self, data) -> str:
        dhash = hashlib.sha256()
        if isinstance(data, (dict, list)):
            encoded = json.dumps(data, sort_keys=True).encode()
        else:
            encoded = str(data).encode()

        dhash.update(encoded)
        return dhash.hexdigest()

    def set_metadata(self) -> None:
        self.metadata["timestamp"] = datetime.datetime.now().timestamp()
        self.metadata["datahash"] = self.hash(self.data)

    def _read(self) -> typing.Tuple[dict, dict]:
        with open(self.file_path) as f:
            d = json.load(f)
        self.has_read = True
        return d["metadata"], d["data"]

    def _write(self):
        self.set_metadata()
        data = {"metadata": self.metadata, "data": self.data}
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value


class Database:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self.documents: typing.Dict[str, Document] = {}
        self.setup(self.database_path)

    def setup(self, path: str):
        files = os.listdir(path)
        for f in files:
            if ".json" in f:
                name = f.split("/")[-1].split(".json")[0]
                self.documents[name] = Document(f)

    def new_document(self, name: str) -> Document:
        """Adds new document to the database"""
        new_doc = Document(self.database_path + f"/{name}.json")
        self.documents[name] = new_doc
        return self.documents[name]

    def sync(self):
        """Syncs all documents in database"""
        for _, doc in self.documents.items():
            doc.sync()

    def __getitem__(self, key: str):
        return self.documents[key]

    def __setitem__(self, key, value):
        if not isinstance(value, Document):
            raise ValueError("set needs to be a nosqllite.Document object")
        self.documents[key] = value
