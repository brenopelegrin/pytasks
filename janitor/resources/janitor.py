from models import *
import time
import werkzeug
import os
max_task_time = int(os.getenv('MAX_TASK_TIME'))
max_storage_time = int(os.getenv('MAX_STORAGE_TIME'))

def RunTaskCleaner():
    print("[janitor] started janitor", flush=True)
    while 1:
        ts_current = time.time()
        
        task = Task.query.filter(Task.created < ts_current-max_storage_time).with_for_update().first()
        if task != None:
            if task.status == "done":
                print(f"[janitor] task {task.id} deleted because it exceeded max storage time", flush=True)
                db.session.delete(task)
                db.session.commit()
            elif task.status == "running" and task.created < ts_current-max_task_time:
                print(f"[janitor] task {task.id} status reassigned to 'waiting' because it exceeded max task time", flush=True)
                task.status = "waiting"
                task.created = task.created+max_task_time
                db.session.commit()
            elif task.status == "waiting":
                db.session.commit()
        else:
            db.session.commit()