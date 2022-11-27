import os
bind = '[::]:8080'
#accesslog = 'gunicorn.log'
#errorlog = 'gunicorn.error.log'
workers = int(os.getenv('GUNICORN_WORKERS'))
threads = int(os.getenv('GUNICORN_THREADS'))
