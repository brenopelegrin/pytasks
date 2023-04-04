FROM python:3.10-slim-bullseye
COPY . /app
ENV DATABASE_URL postgres://postgres:123@localhost:5432/flask_tasks_v2
ENV AMQP_URL redis://localhost:6379
ENV WORKER_NAME worker
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app
RUN cd /app
ENTRYPOINT celery --app=app worker --loglevel=INFO --hostname=$WORKER_NAME@%h