#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = storage.all(State)[0].id
print("First state: {}".format(storage.search(first_state_id, State)))
