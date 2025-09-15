import os
import typing
import warnings
from pathlib import Path
from nosqllite import document
import shutil


class Group:
    def __init__(self, file_path: str) -> None:
        self.file_path = str(os.path.abspath(file_path))
        if file_path[-1] != "/":
            self.file_path += "/"
        self.name = os.path.basename(file_path).split("/")[-1]
        self.documents: typing.Dict[str, typing.Union[document.Document, Group]] = dict()
        self.load(self.file_path)

    @staticmethod
    def new(file_path):
        """Make a new database"""
        if os.path.isdir(file_path):
            warnings.warn("there is a dir with that name")
        else:
            os.mkdir(file_path)
        return Group(file_path)

    def add_group(self, name:str):
        """ add a group (dir) """
        self.documents[name] = Group.new(self.file_path + name)
        return self.documents[name] 

    def load(self, path: str):
        """Load in all documents in database"""
        files = os.listdir(path)
        if path[-1] != "/":
            path += "/"
        for f in files:
            if ".json" in f:
                name = f.split("/")[-1].split(".json")[0]
                self.documents[name] = document.Document.load(path + f)

    def add_document(self, name: str) -> document.Document:
        """Adds new document to the database"""
        if name in self.documents:
            warnings.warn("tried to make new doc but name taken")
            if isinstance(self.documents[name], Group):
                raise LookupError("Error tried to add document with same name as groups")
            return self.documents[name]
        new_doc = document.Document(self.file_path + f"{name}.json")
        self.documents[name] = new_doc
        return self.documents[name]

    def save(self):
        """saves all documents in database"""
        for _, doc in self.documents.items():
            doc.save()

    def delete_document(self, doc_name: str):
        assert doc_name in self.documents, f"Did not find document: {doc_name}"
        self.documents[doc_name].delete()
        del self.documents[doc_name]

    def delete(self):
        """delete database"""
        for itm in self.documents.values():
            itm.delete()

        shutil.rmtree(self.file_path)


    def __getitem__(self, key: str):
        return self.documents[key]

    def __setitem__(self, key, value):
        if not isinstance(value, document.Document):
            raise ValueError("set needs to be a nosqllite.Document object")
        self.documents[key] = value

    def __iter__(self):
        for _, d in self.documents.items():
            yield d

    def __str__(self) -> str:
        return f"{self.file_path}"

    def __repr__(self) -> str:
        return f"nosqllite.group({self.file_path})"

    
