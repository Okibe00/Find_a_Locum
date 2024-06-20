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
    jb_list = storage.all(Job)
    for obj in jb_list:
        if obj.prof_id in prof_ids:
            fil_list.append(obj.to_dict())
    return fil_list

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


@api.route('/post_job', methods=['POST'])
def _post():
    '''returns the new state with status code 201'''
    try:
        post = dict(request.form)
        start_time = post.get("start_t")
        end_time = post.get("end_t")
        prof_list = storage.all(Profession)
        for prof in prof_list:
            if prof.name == post.get("prof"):
                print("before")
                #post.update({"prof_id": prof['id']})
                post["prof_id"] = prof.id
                print("after")
        '''profession doesen't exist'''
        if post.get("prof_id", 0) == 0:
            new_prof = Profession(name=post.get("prof"))
            post['prof_id'] = new_prof.id
            new_prof.save()
        post['Shift'] = f"{start_time} - {end_time}"
        new_job = Job(**post)
        new_job.save()
        return new_job.to_dict()
    except Exception:
        abort(400, description="Not a valid Json")
