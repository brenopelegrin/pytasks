import os
accesslog = 'gunicorn.log'
errorlog = 'gunicorn.error.log'
capture_output = True
workers = int(os.getenv('GUNICORN_WORKERS'))
threads = int(os.getenv('GUNICORN_THREADS'))
#bind = '127.0.0.1:80'
