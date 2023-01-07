from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from celery import Celery
import time as time
import os
from resources.auth import authorized_task

database_url=os.getenv('DATABASE_URL').replace('postgres', 'postgresql', 1)
amqp_url=os.getenv('AMQP_URL')
app = Celery('tasks', backend='db+'+database_url, broker=amqp_url)
app.conf.task_default_queue = 'tasks'

@app.task
def add(x: int, y: int):
    return None

@app.task
def mov3d(dt: float, r0: list, v0: list, mass: float, radius: float, drag: bool):
    return None

@authorized_task
@app.task
def myProtectedTask(x: int, y: int):
    return None