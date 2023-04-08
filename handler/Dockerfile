FROM python:3.10-slim-bullseye
COPY . /app
ENV DATABASE_URL postgres://postgres:123@localhost:5432/flask_tasks_v2
ENV AMQP_URL redis://localhost:6379
ENV WORKER_NAME worker
ENV ENVIRONMENT handler
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN python /app/tasks/manager/manager.py -i physicsjs test --handler /app
WORKDIR /app
RUN cd /app
ENTRYPOINT celery --app=celeryapp worker --loglevel=INFO --hostname=$WORKER_NAME@%h