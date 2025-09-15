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


def test_group():
    db = get_db()
    group = db.add_group("sub")
    doc = group.add_document("sub_doc")
    assert group.name == "sub" 
    doc.data = {"key": "test value"}
    db.save()


def test_group_delete(): 
    global DB_NAME
    db = get_db()
    db.delete()
    assert not os.path.isdir(DB_NAME)

