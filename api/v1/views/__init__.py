'''setting up blueprint'''
from flask import Blueprint

api = Blueprint('app_views', __name__, url_prefix="/api/v1")
# from api.v1.views.index import *
# from api.v1.views.job import *
from . import index,  job

__all__ = ['api', 'index', 'job']
"""
what i want to achieve
separate blueprint for each api
"""
