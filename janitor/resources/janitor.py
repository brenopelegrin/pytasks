from models import *
import time
import werkzeug
import os
max_task_time = float(os.getenv('MAX_TASK_TIME'))

def RunTaskCleaner():
    print("[janitor] started janitor", flush=True)
    while 1:
        ts_current = time.time()
        
        task = Task.query.filter(Task.created < ts_current-max_task_time).with_for_update().first()
        if task != None:
            if task.status == "done":
                print(f"[janitor] task {task.id} deleted because it exceeded max storage time", flush=True)
                db.session.delete(task)
                db.session.commit()
            elif task.status == "running":
                print(f"[janitor] task {task.id} status reassigned to 'waiting' because it exceeded max storage time", flush=True)
                task.status = "waiting"
                db.session.commit()
            elif task.status == "waiting":
                db.session.commit()
        else:
            db.session.commit()