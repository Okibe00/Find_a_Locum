'''create an instance of storage class and reloads data from db/fs'''
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DB_storage
from os import getenv


storage_type = getenv("STORAGE_ENGINE")

if storage_type == 'db':
    storage = DB_storage()
elif storage_type == 'fs':
    storage = FileStorage()
'''if a storage engine  is provided then make tables'''
if storage_type:
    storage.reload()
