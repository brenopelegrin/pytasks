FROM python:3.10-slim-bullseye
COPY . /app
ENV DATABASE_URL postgres://postgres:123@localhost:5432/flask_tasks
ENV MAX_TASK_TIME 30
ENV MAX_STORAGE_TIME 86400
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD [ "python", "/app/janitor.py" ]

