from . import api
from models import storage
from flask import request
from models import storage
from models.job import Job
from models.profession import Profession
from flask import abort


@api.route('/job_search', methods=['POST'])
def filter_jobs():
    """
    Request is going to come with a list json dict of filter criteria
    {prof: [prof_ids]}
    based on this ids you are to return jobs with stated profession id
    """
    '''
    # implement some error handling
        # Case: request.get_json fails
        # Case: storage.all(fails)
        # Case: An empty request is passed
    '''
    post = request.get_json()
    prof_ids = post.get("prof_id")
    fil_list = list()
    '''should refactor to use a list comprehension'''
    jb_list = storage.all('Job')
    for obj in jb_list:
        if obj.prof_id in prof_ids:
            fil_list.append(obj)
    return fil_list

@api.route('/jobs', methods=['GET'])
def list_jobs():
    '''list all jobs in storage'''
    res = storage.all('Job')
    return res


@api.route('/jobs/<job_id>', methods=['GET', 'DELETE'])
def find_job(job_id):
    '''retrieve a job object'''
    job = storage.get('Job', o_id=job_id)
    if job:
        if request.method == 'GET':
            if job:
                return job
        elif request.method == 'DELETE':
            if storage.delete(job_id):
                return {'status': 200}
    abort(404)


@api.route('/post_job', methods=['POST'])
def _post():
    '''Add a job to storage
    
    '''
    pass
