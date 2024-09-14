from models.city import City
from models.state import State
from models.profession import Profession
from models.user import User
from models.job import Job
from models import storage

'''creating jobs'''
state = storage.get('State', 'Lagos')
print(state)
s_id = state[0]['id']
state_id = storage.get('State', o_id=s_id)
print(state_id)
exit()
city = storage.get('City', 'Lagos')
prof = storage.get('Profession', 'Pharmacist')
user = storage.get('User', 'Okibe Onmeje')
f_job = {
    "title": "Locum pharmacist",
    "address": "14 Yaya Abatan road ogba ikeja Lagos Nigeria",
    "state_id": f"{state[0].get('id')}",
    "city_id": f"{city[0]['id']}",
    "profession_id": f"{prof[0]['id']}",
    "user_id": f"{user[0]['id']}",
    "hourly_rate": "1000",
    "status": "Open",
    "shift": f"2:00pm - 4:00pm",
    "premise_name": "Pharmabay limited",
    "description": "Provide pharmaceutical services for  patients",
    'hours_per_shift': "3"
}
print(f_job)
job_0 = Job(**f_job)

#for obj in objs:
storage.save(job_0)
