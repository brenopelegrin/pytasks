FROM python:3.10-slim-bullseye
COPY . /app
ENV DATABASE_URL postgres://postgres:123@localhost:5432/flask_tasks_v2
ENV AMQP_URL redis://localhost:6379
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app
RUN cd /app
ENTRYPOINT ["celery", "--app=tasks", "worker", "--loglevel=INFO", "--hostname=worker1@%h"]