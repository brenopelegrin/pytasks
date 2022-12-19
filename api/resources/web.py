from flask_restful import reqparse, abort, Api, Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser
from flask import jsonify, render_template, make_response, render_template_string
import werkzeug
from server import frontend_url
import os
from celery.result import AsyncResult

#######################################################
#       Collect task list, args and arg types
#######################################################
from tasks import app as capp
import inspect
celery_tasks = capp.tasks

def collect_tasks(celery_task_list):
    tasklist = {}
    for name in celery_task_list.keys():
        if 'task' in name:
            tasklist[name.replace('tasks.', '')] = {
                'task': celery_task_list[name], 
                'func': celery_task_list[name].__wrapped__,
                'args': inspect.getfullargspec(celery_task_list[name].__wrapped__).annotations
                }
    return tasklist

tasklist = collect_tasks(celery_tasks)
#######################################################
        
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

class NewTask(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', required=True, type=str, help='You need to inform required_arg', location='json')
        parser.add_argument('args', required=True, type=dict, help='You need to inform args dict', location='json')
        args = parser.parse_args()

        abort_if_tasktype_doesnt_exist(tasktype=args["type"])
        abort_if_task_params_are_invalid(tasktype=args["type"], given_params=args["args"])

        try:
            task_class = tasklist[args["type"]]['task']
            task = task_class.delay(**args["args"])
            return {"id": task.id, "type": args["type"], "status": task.state}
        except Exception as exc:
            return{"error": str(exc)}

class ViewTask(Resource):
    def get(self, task_id):
        try:
            task = AsyncResult(task_id, app=capp)
            if task.state == "SUCCESS":
                return {"id": task.id, "status": task.state, "result": task.get()}
            else:
                return {"id": task.id, "status": task.state, "result": {}}
        except Exception as exc:
            return{"error": str(exc)}

class Ping(Resource):
    def get(self):
        return {"status": "online"}
