from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from celery import Celery
import time as time
import os
from functools import wraps

database_url=os.getenv('DATABASE_URL').replace('postgres', 'postgresql', 1)
amqp_url=os.getenv('AMQP_URL')
default_task_queue = os.getenv('DEFAULT_TASK_QUEUE')
celery_app = Celery(default_task_queue, backend='db+'+database_url, broker=amqp_url)
celery_app.conf.task_default_queue = default_task_queue
celery_app.config_from_object('celeryconfig')

from resources.auth import authorized_task

global_decorators = {
    'authorized_task': authorized_task
}

from tasks import exports

exports.init(celery_app, **global_decorators)

celery_tasks = celery_app.tasks