#!/bin/python3
from models import storage
from models.city import City
from models.state import State



objs = storage.all(State)
print(len(objs))
for obj in objs:
    if obj.__class__ == State:
        print(obj.cities)





