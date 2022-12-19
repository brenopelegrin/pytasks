FROM python:3.10-slim-bullseye
COPY . /app
ENV DATABASE_URL postgres://postgres:123@localhost:5432/flask_tasks_v2
ENV AMQP_URL redis://localhost:6379
ENV FRONTEND_URL *
ENV GUNICORN_WORKERS 3
ENV GUNICORN_THREADS 1
EXPOSE 8080
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app
ENTRYPOINT gunicorn --conf /app/gunicorn.conf.py app:app

