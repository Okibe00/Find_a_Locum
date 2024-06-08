'''describes the state object'''
from models.base_model import BaseModel
from models.city import City


class State(BaseModel):
    '''state class'''
    @property
    def cities(self):
        '''
        return a list of all city objects linked to current state
        '''
        from models import storage
        state_id = self.id
        all_objects = storage.all(City)
        cities = list()
        for obj in all_objects:
            if state_id == obj.state_id:
                cities.append(obj)

        return cities
