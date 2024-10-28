
import os
import typing
import json
import datetime
import decimal
import hashlib
import warnings


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
        self.file_path = file_path
        if not self.is_doc(file_path):
            self._write(self.file_path, self.set_metadata(), self.data)

        self.metadata, self.data = self._read(self.file_path)
        #self.file_path = os.path.abspath(file_path)
        self.has_read = True

    @staticmethod
    def is_doc(file_path) -> bool:
        if not os.path.isfile(file_path) or not ".json" in file_path:
            return False
        with open(file_path) as f:
            d = json.load(f)
        if not "data" in d or not "metadata" in d:
            return False
        del d
        return True

    def sync(self) -> None:
        m, _ = self._read(self.file_path)
        if m["datahash"] == self.hash(self.data):
            return
        else:
            self._write(self.file_path, self.set_metadata(), self.data)

    def hash(self, data) -> str:
        dhash = hashlib.sha256()
        if isinstance(data, (dict, list)):
            encoded = json.dumps(data, sort_keys=True).encode()
        else:
            encoded = str(data).encode()
        dhash.update(encoded)
        return dhash.hexdigest()

    def set_metadata(self) -> dict:
        self.metadata["timestamp"] = datetime.datetime.now().timestamp()
        self.metadata["datahash"] = self.hash(self.data)
        return self.metadata


    @staticmethod
    def _read(file_path) -> typing.Tuple[dict, typing.Union[list, dict]]:
        with open(file_path) as f:
            d = json.load(f)
        return d["metadata"], d["data"]

    @staticmethod
    def _write(file_path:str, metadata:dict, data:typing.Union[list, dict]) -> None:
        d = {
            "metadata": metadata, 
            "data": data
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=4)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value


class Database:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self.documents: typing.Dict[str, Document] = {}
        self.setup(self.database_path)

    @staticmethod
    def new(file_path):
        if os.path.isdir(file_path): 
            raise NameError("there is a dir with that name")
        os.mkdir(file_path)
        return Database(file_path)

    def setup(self, path: str): 
        files = os.listdir(path)
        for f in files:
            if ".json" in f:
                name = f.split("/")[-1].split(".json")[0]
                self.documents[name] = Document(f)

    def new_document(self, name: str) -> Document:
        """Adds new document to the database"""
        if name in self.documents:
            warnings.warn("tried to make new doc but name taken")
            return self.documents[name]
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