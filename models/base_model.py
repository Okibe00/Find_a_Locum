'''base model class'''
from uuid import uuid4
from datetime import datetime
import models


class BaseModel():
    '''defines all common attributes and methods'''
    def __init__(self, *args, **kwargs):
        '''instantiate an object'''
        if args:
            print('Usage: Basemodel(Attr0=value,...)')
        if kwargs:
            for k, v in kwargs.items():
                if k != '__class__':
                    if k in ['created_at', 'updated_at']:
                        fmt = '%Y-%m-%dT%H:%M:%S.%f'
                        setattr(self, k, datetime.strptime(v, fmt))
                    else:
                        setattr(self, k, v)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        '''generate id is not passed'''
        if self.__dict__.get('id', 0):
            pass
        else:
            self.id = str(uuid4())
        '''generated updated and created date and time'''
        if self.__dict__.get('updated_at', 0) == 0:
            self.updated_at = datetime.now()
        if self.__dict__.get('created_at', 0) == 0:
            self.created_at = datetime.now()
        models.storage.new(self)

    def __str__(self):
        '''print the string representation of an obj'''
        name = self.__class__.__name__
        inst_id = self.id
        attr = dict(self.__dict__)
        rep = f'[{name}] ({inst_id}) {attr}'
        return (rep)

    def save(self):
        '''
        updates the public instance attribute updated_at
        with the current datetime
        '''
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        '''
        returns a dictionary containing all keys/values of
        __dict__ of the instance:
        '''
        new_obj = dict(self.__dict__)
        cls_name = self.__class__.__name__
        new_obj.update({'__class__': f'{cls_name}'})
        fmt_updated_at = new_obj['updated_at'].strftime('%Y-%m-%dT%H:%M:%S.%f')
        fmt_created_at = new_obj['created_at'].strftime('%Y-%m-%dT%H:%M:%S.%f')
        new_obj['created_at'] = fmt_created_at
        new_obj['updated_at'] = fmt_updated_at
        return (new_obj)
