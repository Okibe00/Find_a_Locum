from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def _status():
    '''return api status'''
    return {'status': 'Ok'}


@app_views.route('/stats')
def _count():
    '''retrieve the number of objects in storage'''
    all_objs = storage.all()
    count_dict = dict()
    for obj in all_objs:
        cls = f'{obj.__class__.__name__}'
        count_dict[f'{cls}'] = count_dict.get(cls, 0) + 1
    return count_dict
