import os
broker_url = os.getenv('AMQP_URL')
imports = ('tasks',)
result_backend = os.getenv('DATABASE_URL').replace('postgres', 'postgresql', 1)
task_serializer = 'json'
task_track_started = True
task_acks_late = True
result_serializer = 'json'
accept_content = ['json']
task_default_queue="tasks"
