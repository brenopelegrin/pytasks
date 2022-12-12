import os
bind = '[::]:8080'
#accesslog = 'gunicorn.log'
#errorlog = 'gunicorn.error.log'
loglevel='info'
workers = int(os.getenv('GUNICORN_WORKERS'))
threads = int(os.getenv('GUNICORN_THREADS'))
