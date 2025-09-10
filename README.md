# nosqllite
A lite nosql database for python 



## Example 


```python
import nosqllite

db = nosqllite.Database.new("demo_db")

doc = db.add_document("users")

db["users"].data = [{"name":"Foo_1"},{"name":"Foo_2"}]

print(db["users"].data[-1]["name"])

db.save() 

print(doc.data)
print(db.documents)
for doc in db:
    print(doc.type_of())
    for d in doc:
        print(d)

db["users"].data.pop(-1)
print(db["users"].data)
db.save()
```

for more check out [my experiments](./expr/expr.ipynb).


## Install 

```bash
pip install nosqllite
```


## Usage

There is only a few things you need to understand:

There is `Database`

```python
import nosqllite

db = nosqllite.Database.new("demo_db")

# or if you have one already you can also 

db = nosqll.Database("demo_db")

# you can also add documents
db.save()
```

A nosql data base i made up of documets, this are json files.

```python
doc = db.add_document("foo") # this have added a json file in the dir ./demo_db/foo.json
```

Then there is groups. Groups are just a dirs.

```python
db.add_group("sub") # this adds a dir into ./demo_db/sub/ 
db["sub"].add_document("subdoc") # this have added a json file in the dir ./demo_db/sub/subdoc.json
db["sub"].add_group("subsub") # this adds a dir into ./demo_db/sub/subsub/ 
db["sub"]["subsub"].add_document("test")
db["sub"]["subsub"]["test"].data["some_key"] = "value"
db.save()
```