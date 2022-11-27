import os
#accesslog = 'gunicorn.log'
#errorlog = 'gunicorn.error.log'
workers = int(os.getenv('GUNICORN_WORKERS'))
threads = int(os.getenv('GUNICORN_THREADS'))
bind = '_local_ip.internal:8000'
