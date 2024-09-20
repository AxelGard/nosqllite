import os
import typing
import json


class Document:
    def __init__(self, file_path:str) -> None:
        self.name = file_path.split("/")[-1].split(".json")[0]
        self._data: typing.Union[list, dict] = {} 
        self._metadata = {}
        self.is_locked = False
        if not Document.is_doc(file_path):
            self.file_path = file_path 
            self._write()
        self._metadata, self._data = self._read()
        self.file_path = os.path.abspath(file_path)
        self.has_read = True

    @staticmethod
    def is_doc(file_path) -> bool:
        return os.path.isfile(file_path) and ".json" in file_path

    def _read(self) -> typing.Tuple[dict,dict]:
        with open(self.file_path) as f: 
            d = json.load(f)  
        return d["meta_data"], d["data"]

    def _write(self):
        data = {"meta_data":self._metadata, "data":self._data}
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def __getitem__(self, key):
        m, d = self._read()
        self._data = d 
        self._metadata = m 
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value


    

class Database: 
    def __init__(self, database_path:str) -> None:
        self.database_path = database_path
        self.documents:typing.Dict[str,Document] = {}

    def new_document(self, name:str) -> Document:
        new_doc = Document(self.database_path + f"/{name}.json")
        self.documents[name] = new_doc
        return self.documents[name]

    def __getitem__(self, key:str):
        return self.documents[key]

    def __setitem__(self, key, value):
        assert isinstance(value, Document)
        self._data[key] = value
    
