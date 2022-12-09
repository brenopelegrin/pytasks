from flask_restful import reqparse, abort, Api, Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser
from models import *
from time import sleep
from flask import jsonify, render_template, make_response, render_template_string
import werkzeug
import time
from base64 import b64encode
import io
from server import frontend_url
from datetime import datetime
import os

from resources.tasks import tasks
tasklist = tasks.list

max_storage_time = float(os.getenv('MAX_STORAGE_TIME'))

def abort_if_tasktype_doesnt_exist(tasktype):
    if tasktype not in tasklist.keys():
        abort(404, message=f'task type {tasktype} doesnt exist')

def abort_if_task_params_are_invalid(tasktype, given_params):
    required_params = tasklist[tasktype]['args']

    # Verify if user passed all required params
    for param in required_params.keys():
        if param in given_params.keys():
            # Verify if the type of passed param matches the required param type
            if type(given_params[param]) != required_params[param]:
                message = f'the passed param {param} doesnt match the required type: {required_params[param]}.'
                abort(404, message=message)
        else:
            message = f'the required param {param} was not passed. '
            abort(404, message=message)

    # Verify if user passed params that are not required
    for param in given_params.keys():
        if param not in required_params.keys():
            message = f'the passed param {param} is not required.'
            abort(404, message=message)

def abort_if_task_doesnt_exist(task_id):
    exists = db.session.query(Task.id).filter_by(id=task_id).scalar() is not None
    if exists != True:
        abort(404, message=f'task id {task_id} is not registered')

class NewTask(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', required=True, type=str, help='You need to inform task type', location='json')
        parser.add_argument('args', required=True, type=dict, help='You need to inform args dict', location='json')
        args = parser.parse_args()

        abort_if_tasktype_doesnt_exist(tasktype=args["type"])
        abort_if_task_params_are_invalid(tasktype=args["type"], given_params=args["args"])

        ts_current = time.time()
        task = Task(type=args["type"], args=args["args"], status="waiting", created=ts_current, expire=ts_current+max_storage_time)
        
        db.session.add(task)
        db.session.commit()
        
        abort_if_task_doesnt_exist(task.id)
        task = Task.query.get(task.id)

        return task_schema.dump(task)

class ViewTask(Resource):
    def get(self, task_id):
        abort_if_task_doesnt_exist(task_id)
        task = Task.query.get(task_id)
        return task_schema.dump(task)

class Ping(Resource):
    def get(self):
        return {"status": "online"}
