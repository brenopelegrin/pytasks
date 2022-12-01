FROM python:3.9.15-alpine3.15
COPY . /app
ENV DATABASE_URL postgres://postgres:123@localhost:5432/flask_tasks
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD [ "python", "/app/handler.py" ]

