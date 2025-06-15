FROM python:3.10-slim-bullseye
COPY . /app
ARG pytasks_taskpacks_manager_INSTALL_PACKAGES
ENV DATABASE_URL postgres://postgres:password@localhost:5432/pytasks
ENV AMQP_URL redis://localhost:6379
ENV FRONTEND_URL *
ENV GUNICORN_WORKERS 3
ENV GUNICORN_THREADS 2
EXPOSE 8080
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN python /app/tasks/manager/manager.py -i physicsjs test --api /app
WORKDIR /app
ENTRYPOINT gunicorn --conf /app/gunicorn.conf.py app:app

