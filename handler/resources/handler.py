from models import *
import time
import werkzeug
import os
import random
from resources.tasks import tasks
tasklist = tasks.list

def RunTask(task_id, type, args):
    print(f"[handler] task {task_id} (type {type}) is running", flush=True)

    #do some logic here
    task_func = tasklist[type]['func']
    result_of_execution = task_func(**args)

    return {"message": result_of_execution}

def TaskHandler():
    print("[handler] started taskhandler", flush=True)

    while 1:
        task = db.session.query(Task).filter_by(status='waiting').with_for_update().first()
        if task != None:
            current_id = task.id
            current_args = task.args
            current_type = task.type
            if current_type in tasklist.keys():
                print(f'[handler] task {current_id} (type {current_type}) is ready to run.', flush=True)
                task.status = "running"
                db.session.commit()
                try:
                    result = RunTask(task_id=current_id, type=current_type, args=current_args)
                    print(f"[handler] task {current_id} is finished", flush=True)

                    task = db.session.query(Task).filter_by(id=current_id).with_for_update().first()
                    task.result = result
                    task.status = "done"
                    db.session.commit()
        
                except:
                    
                    print(f"[handler] task {current_id} (type {current_type}) failed to run", flush=True)

                    task = db.session.query(Task).filter_by(id=current_id).with_for_update().first()
                    if task != None:
                        task.result={"message:" "error when running"}
                        task.status = "waiting"
                        db.session.commit()
            else:
                print(f"[handler] task {current_id} has invalid type ({current_type}), the handler will not run it.")