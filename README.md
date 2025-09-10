# nosqllite
A lite nosql database for python 



## Example, Demo 


```python
import nosqllite as nosqll

db = nosqll.Database.new("demo_db")

doc = db.new_document("users")

db["users"].data = [{"name":"Foo_1"},{"name":"Foo_2"}]

db.save() 

print(doc.data)
print(db.documents)
for d in db:
     
```