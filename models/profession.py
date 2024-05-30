'''describes the profesion object'''
from models.base_model import BaseModel


class Profession(BaseModel):
    '''profession class'''
    def __init__(self, *args, **kwargs):
        '''Set instance attributes'''
        if kwargs:
            super.__init__(*args, **kwargs)
        else:
            print("Please state profession")
