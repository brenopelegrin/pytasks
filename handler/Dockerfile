FROM python:3.10-slim-bullseye
COPY . /app
ARG pytasks_taskpacks_manager_INSTALL_PACKAGES
ENV DATABASE_URL postgres://postgres:password@localhost:5432/pytasks
ENV AMQP_URL redis://localhost:6379
ENV WORKER_NAME worker
ENV ENVIRONMENT handler
ENV DEFAULT_TASK_QUEUE tasks
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN python /app/tasks/manager/manager.py -i test subtitles --handler /app
WORKDIR /app
RUN cd /app
ENTRYPOINT celery --app=celeryapp worker --loglevel=INFO --hostname=$WORKER_NAME@%h
