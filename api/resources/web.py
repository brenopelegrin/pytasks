from flask_restful import reqparse, abort, Api, Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser
from flask import jsonify, render_template, make_response, render_template_string
import werkzeug
from server import frontend_url
import os
from celery.result import AsyncResult
from resources.auth import require_jwt, generate_new_jwt, decrypt_jwt_authorization_header, verify_credentials, get_user_permissions, abort_if_authorization_header_not_present, abort_if_jwt_is_invalid

#######################################################
#       Collect task list, args and arg types
#######################################################
from celeryapp import celery_app as capp
from resources.auth import authorizedTasks
import inspect
celery_tasks = capp.tasks

def collect_tasks(celery_task_list):
    tasklist = {}
    for name in celery_task_list.keys():
        if 'tasks.packs.' in name:
            pure_name = name.replace('tasks.packs.', '')
            auth_data = {}
            if pure_name in authorizedTasks.list:
                auth_data = authorizedTasks.auth_data[pure_name]
            tasklist[pure_name] = {
                'task': celery_task_list[name], 
                'func': celery_task_list[name].__wrapped__,
                'args': inspect.getfullargspec(celery_task_list[name].__wrapped__).annotations,
                'auth_data': auth_data
                }
    return tasklist

tasklist = collect_tasks(celery_tasks)
#######################################################

def abort_if_credentials_are_invalid(user, password):
    is_valid = verify_credentials(user, password)
    if not is_valid:
        abort(401, message=f"Your credentials are invalid.")

def abort_if_doesnt_have_permission(tasktype, auth_header):
    if(tasktype in authorizedTasks.list):
        if(auth_header):
            decrypted_payload = decrypt_jwt_authorization_header(auth_header)
            try:
                task_permission = decrypted_payload['allowed_tasks'][tasktype]
            except:
                abort(401, message=f"The payload in your JWT is not valid.")

            if not task_permission:
                abort(401, message=f"You don't have permission to use this tasktype.")
        else:
            abort_if_authorization_header_not_present()
        
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
    """
    Registers a new task request through POST method.
    """
    def post(self):
        """Posts a task 

        Returns:
            taskInfo (dict): dictionary with the task id, arguments passed and current status of the task. 
        """
        parser = reqparse.RequestParser()
        parser.add_argument('type', required=True, type=str, help='You need to inform type', location='json')
        parser.add_argument('args', required=True, type=dict, help='You need to inform args dict', location='json')
        parser.add_argument('Authorization', location='headers')
        args = parser.parse_args()

        abort_if_tasktype_doesnt_exist(tasktype=args["type"])
        abort_if_doesnt_have_permission(tasktype=args["type"], auth_header=args["Authorization"])
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

class ProtectedByJwt(Resource):
    method_decorators = {'get': [require_jwt]}
    def get(self, decoded_payload):
        parser = reqparse.RequestParser()
        args = parser.parse_args()

        return decoded_payload

class GenerateTokenForUser(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user', required=True, type=str, help='You need to inform user', location='json')
        parser.add_argument('password', required=True, type=str, help='You need to inform password', location='json')
        args = parser.parse_args()

        abort_if_credentials_are_invalid(user=args["user"], password=args["password"])

        payload = get_user_permissions(user=args["user"], password=args["password"])

        token, expire = generate_new_jwt(payload)

        return {"token": token, "exp": expire}

class ViewTaskList(Resource):
    def get(self):
        return_tasklist = {}
        for task in tasklist:
            return_args = {}
            for arg in tasklist[task]["args"]:
                return_args[arg] = str(tasklist[task]["args"][arg])
            
            need_auth = False
            if task in authorizedTasks.list:
                need_auth = True

            return_tasklist[task] = {"require_authorization": need_auth, "args": return_args}

        return return_tasklist

