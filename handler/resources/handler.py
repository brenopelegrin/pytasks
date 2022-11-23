from models import *
import time
import werkzeug
import os
max_task_time = float(os.getenv('MAX_TASK_TIME'))

def ExecuteWhenRunningTask(task_id, args):
    return "none"

def RunTask(task_id, args):
    print(f"[handler] task {task_id} is running", flush=True)

    #do some logic here
    result_of_execution = ExecuteWhenRunningTask(task_id, args)

    return {"message": result_of_execution}

def TaskHandler():
    print("[handler] started taskhandler", flush=True)

    while 1:
        task = db.session.query(Task).filter_by(status='waiting').with_for_update().first()
        if task != None:
            current_id = task.id
            current_args = task.args
            print(f'[handler] task {current_id} is ready to run.', flush=True)
            task.status = "running"
            db.session.commit()

            try:
                result = RunTask(task_id=current_id, args=current_args)
                print(f"[handler] task {current_id} is finished", flush=True)

                task = db.session.query(Task).filter_by(id=current_id).with_for_update().first()
                task.result = result
                task.status = "done"
                db.session.commit()

            except:
                
                print(f"[handler] task {current_id} failed to run", flush=True)

                task = db.session.query(Task).filter_by(id=current_id).with_for_update().first()
                if task != None:
                    task.result={"message:" "error when running"}
                    task.status = "waiting"
                    db.session.commit()