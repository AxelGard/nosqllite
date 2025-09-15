import os
import typing
import json
import datetime
import hashlib


class Document:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.name = os.path.basename(file_path).split("/")[-1].split(".json")[0]
        self.data: typing.Union[list, dict] = {}
        self.metadata = {}
        self.is_locked = False
        if not self.is_doc(file_path):
            self._write(self.file_path, self.set_metadata(), self.data)

        self.metadata, self.data = self._read(self.file_path)
        self.has_read = True

    @staticmethod
    def is_doc(file_path: str) -> bool:
        """is document a valid doc?"""
        if not os.path.isfile(file_path) or not file_path.endswith(".json"):
            return False
        with open(file_path) as f:
            d = json.load(f)
        if not "data" in d or not "metadata" in d:
            return False
        del d
        return True

    def save(self) -> None:
        m, _ = self._read(self.file_path)
        if m["datahash"] == self.hash(self.data):
            return
        else:
            self._write(self.file_path, self.set_metadata(), self.data)

    def delete(self) -> None:
        self.data = dict()
        self.metadata = dict()
        os.remove(self.file_path)

    @staticmethod
    def hash(data) -> str:
        dhash = hashlib.sha256()
        if isinstance(data, (dict, list)):
            encoded = json.dumps(data, sort_keys=True).encode()
        else:
            encoded = str(data).encode()
        dhash.update(encoded)
        return dhash.hexdigest()

    def type_of(self):
        return type(self.data)

    def set_metadata(self) -> dict:
        self.metadata["timestamp"] = datetime.datetime.now().timestamp()
        self.metadata["datahash"] = self.hash(self.data)
        return self.metadata

    @staticmethod
    def load(file_path):
        if not Document.is_doc(file_path):
            raise ValueError(f"Tried to load a non Doc file: {file_path}")
        return Document(file_path)

    @staticmethod
    def _read(file_path) -> typing.Tuple[dict, typing.Union[list, dict]]:
        with open(file_path) as f:
            d = json.load(f)
        return d["metadata"], d["data"]

    @staticmethod
    def _write(file_path: str, metadata: dict, data: typing.Union[list, dict]) -> None:
        d = {"metadata": metadata, "data": data}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=4)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        print("debug")
        self.data[key] = value

    def __iter__(self):
        for v in self.data:
            yield v

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return f"nosqllite.Document({self.file_path})"

    def __dict__(self):
        return dict({
            "data": self.data,
        })
