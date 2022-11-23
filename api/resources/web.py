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
max_task_time = float(os.getenv('MAX_TASK_TIME'))

def abort_if_task_doesnt_exist(task_id):
    exists = db.session.query(Task.id).filter_by(id=task_id).scalar() is not None
    if exists != True:
        abort(404, message=f'task id {task_id} is not registered')

class NewTask(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('required_arg', required=True, type=str, help='You need to inform required_arg', location='json')
        args = parser.parse_args()
        ts_current = time.time()
        task = Task(required_arg=args["required_arg"], args=args, status="waiting", created=ts_current, expire=ts_current+max_task_time)
        
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
