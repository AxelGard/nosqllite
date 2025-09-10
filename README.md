# nosqllite
A lite nosql database for python 



## Example 


```python
import nosqllite as nosqll

db = nosqll.Database.new("demo_db")

doc = db.new_document("users")

db["users"].data = [{"name":"Foo_1"},{"name":"Foo_2"}]

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
