from . import api
from models import storage
from flask import request
from models import storage
from models.job import Job
from flask import abort


@api.route('/job_search', methods=['POST'])
def filter_jobs():
    """
    Request is going to come with a list json dict of filter criteria
    {prof: [prof_ids]}
    based on this ids you are to return jobs with stated profession id
    """
    try:
        post = request.get_json()
        prof_ids = post["prof_id"]
        fil_list = list()
        '''should refactor to use a list comprehension'''
        for obj in storage.all(Job):
            if obj.prof_id in prof_ids:
                fil_list.append(obj.to_dict())
        return fil_list
    except Exception:
        abort(400, description="Not a valid JSON")


@api.route('/jobs', methods=['GET'])
def list_jobs():
    '''list all jobs in storage'''
    jobs_list = storage.all(Job)
    jobs_dict = list()
    for job in jobs_list:
        jobs_dict.append(job.to_dict())

    return jobs_dict


@api.route('/jobs/<job_id>', methods=['GET', 'DELETE'])
def find_job(job_id):
    '''retrieve a job object'''
    job = storage.search(job_id, Job)
    if job:
        if request.method == 'GET':
            if job:
                return job.to_dict()
        elif request.method == 'DELETE':
            if storage.delete(job_id):
                return {'status': 200}
    abort(404)


@api.route('/jobs', methods=['POST'])
def _post():
    '''returns the new state with status code 201'''
    try:
        post = request.get_json()
    except Exception:
        abort(400, description="Not a valid Json")

    if post.get('title', 0):
        new_job = Job(**post)
        return new_job.to_dict()
    else:
        abort(400, description='Missing Job title')
