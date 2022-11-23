FROM python:3.9.15-alpine3.15
COPY . /app

ENV API_URL http://localhost:8000/task/new

WORKDIR /app
CMD [ "python", "/app/tester.py" ]