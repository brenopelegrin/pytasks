FROM python:3.10-slim-bullseye
COPY . /app
ENV DATABASE_URL postgres://postgres:123@localhost:5432/flask_tasks
ENV FRONTEND_URL http://localhost:3000
ENV GUNICORN_WORKERS 3
ENV GUNICORN_THREADS 1
ENV MAX_STORAGE_TIME 86400
EXPOSE 8080
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app
CMD [ "gunicorn", "--conf", "/app/gunicorn.conf.py", "app:app"]

