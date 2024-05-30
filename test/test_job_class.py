#!/bin/python3
from models.job import Job
from datetime import datetime, time
job_dict = {
    'Title': 'Locum pharmacist',
    'description': ''
}
my_model = Job()
my_model.title = 'locum pharmacist'
my_model.rate = 500
my_model.start_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
my_model.status = 'open'
my_model.employer_contact = '07085888721'
my_model.state_date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
my_model.end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
my_model.opening_time= time.fromisoformat('08:00:00').strftime("%H:%M:%S")
my_model.closing_time = time.fromisoformat('09:00:00').strftime("%H:%M:%S")
my_model.description = 'the locum pharmacist will dispens and consult pxt for said period'
print(my_model)
my_model.save()
print("---")
print(my_model)
my_model_json = my_model.to_dict()
print("---")
print(my_model_json)
print("---")
print("JSON of my_model:")
for key in my_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))
