import nosqllite 
import os

DB_NAME = "./tests/my-nosql-lite-db"

def get_db() -> nosqllite.Database:
    global DB_NAME
    if not os.path.exists(DB_NAME):
        db = nosqllite.Database.new(DB_NAME)
    else: 
        db = nosqllite.Database(DB_NAME)
    return db


def test_database():
    db = get_db()
    assert db.name == "my-nosql-lite-db" 



def test_database_delete():
    global DB_NAME
    db = get_db()
    db.new_document("test_1")
    db.new_document("test_2")
    db["test_1"].data = [1,2,3]
    db["test_2"].data = [1,2,3]
    db.save()
    assert os.path.isdir(DB_NAME)
    assert os.path.isfile(f"{DB_NAME}/test_1.json") 

    db.delete_document("test_1")
    assert not os.path.isfile(f"{DB_NAME}/test_1.json") 

    db.delete()
    assert not os.path.isdir(DB_NAME)
    