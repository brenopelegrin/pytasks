FROM python:3.9.15-alpine3.15
COPY . /app
ENV DATABASE_URL postgres://postgres:123@localhost:5432/flask_tasks
ENV BACKEND_URL http://localhost:5000
ENV FRONTEND_URL http://localhost:3000
ENV MAX_TASK_TIME 30
ENV GUNICORN_WORKERS 3
ENV GUNICORN_THREADS 1
EXPOSE 8080
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app
CMD [ "gunicorn", "--conf", "/app/gunicorn.conf.py", "app:app"]

