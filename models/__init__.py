'''create an instance of storage class and reloads data from db/fs'''
from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
