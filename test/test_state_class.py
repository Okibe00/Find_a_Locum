#!/bin/python3
from models.state import State
from models import storage
my_state = State()
my_state.name = "Lagos"
print(my_state)
print(storage.all())
my_model_json = my_state.to_dict()
print(my_model_json)
print("JSON of my_model:")
for key in my_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))
