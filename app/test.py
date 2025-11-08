import json

data = {'id': 2, 'name': 'Int', 'info': 'integer type', 'time': '2025-10-14T15:04:32.561527'}

print(json.dumps(data))
import datetime

print(datetime.date.ctime)
car = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}

x = car.keys()
#print(x)

car["color"] = "white"
#print(car.keys()) 
#print(car.values())
for i, (key, value) in enumerate(car.items()):
	print(i, key, value)
 
k =  {key: bool(i & (1 << i)) for i, key in enumerate(data.keys())}
print(k)

flags_map = {
        "cantBeDeleted": False,
        "canDoMathOperation": False,
        "canDoLogicalOperation": True,
        "isIterable": False,
        "isDeleted": False,
    }

flag= 16
checked = {}

for i, key in enumerate(flags_map.keys()):
	k = bool(flag & (1<<i))
	checked[key] = k
 
print(checked)