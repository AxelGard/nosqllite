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
