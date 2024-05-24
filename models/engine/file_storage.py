'''File storage engine'''
import json
from os.path import exists
from models.base_model import BaseModel
from models.state import State
from models.job import Job


classes = {
        'BaseModel': BaseModel,
        'Job': Job,
        'State': State
    }


class FileStorage():
    '''file storage class'''
    __file_path = ''
    __objects = dict()

    def all(self, cls=None):
        '''return the dictionary __objects'''
        if cls is None:
            return self.__objects
        else:
            try:
                sel_objs = []
                for k, v in self.__objects.items():
                    if v.__class__.__name__ == cls or v.__class__ == cls:
                        sel_objs.append(v)
                return sel_objs
            except Exception:
                pass

    def new(self, obj):
        """
        new(self, obj): sets in __objects the obj with key
        <obj class name>.id
        """
        obj_id = obj.id
        obj_cls = obj.__class__.__name__
        key = f'{obj_cls}.{obj_id}'
        self.__objects[key] = obj

    def save(self):
        """
        serializes __objects to the JSON file (path: __file_path)
        """
        temp_dict = {}
        try:
            with open('storage.json', 'w') as fp:
                for key in self.__objects:
                    temp_dict[key] = self.__objects[key].to_dict()
                json.dump(temp_dict, fp, indent=4)
        except Exception as e:
            print(f'Failed to open file: {e}')

    def reload(self):
        '''
         deserializes the JSON file to __objects
         (only if the JSON file (__file_path) exists;
         otherwise, do nothing. If the file doesn’t exist,
         no exception should be raised)
        '''
        if exists('storage.json'):
            try:
                with open('storage.json') as fp:
                    loaded_dict = json.load(fp)
                    for k, v in loaded_dict.items():
                        cls_name = v['__class__']
                        self.__objects[k] = classes[cls_name](**v)
            except Exception as e:
                pass
        else:
            pass
