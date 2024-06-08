#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.state import State

all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new object --")
my_model = State()
my_model.name = "Lagos"
my_model.lgc = 'Ikeja'
my_model.save()
print(my_model)
