from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from celery import Celery
import time as time
import os
from resources.auth import authorized_task

database_url=os.getenv('DATABASE_URL').replace('postgres', 'postgresql', 1)
amqp_url=os.getenv('AMQP_URL')
celery_app = Celery('tasks', backend='db+'+database_url, broker=amqp_url)
celery_app.conf.task_default_queue = 'tasks'

global_decorators = {
    'authorized_task': authorized_task
}

from tasks import exports

exports.init(celery_app, **global_decorators)