---
title: Setting up
---

# Setting up pytasks

First, you should clone the repository and go to the cloned repository:

```bash
git clone https://github.com/brenopelegrin/pytasks.git &&
cd pytasks && export PYTASKS_DIR=$(pwd)
```

## Configuring ``api``
### Generating your RSA keys for API authentication

Make sure you have ``ssh-keygen`` and ``openssl`` installed. Then, run the following command to generate 4096-bit RSA public and private keypair for API:

```bash
cd $PYTASKS_DIR && mkdir keys && cd keys &&
ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key &&
openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub
```

After that, your keys will be available inside the ``pytasks/keys/`` directory. The private key is ``jwtRS256.key`` and the public key is ``jwtRS256.key.pub``.

### Setting up environment variables for API

#### Using .env file (recommended)
For this, you can modify the ``pytasks/api.env`` file and configure your env variables in the format ``KEY=VALUE``.

For example:

```bash title="api.env"
DATABASE_URL=postgres://user:password@ip:5432/pytasks
AMQP_URL=amqp://user:password@ip:5672
FRONTEND_URL=*
GUNICORN_WORKERS=3
GUNICORN_THREADS=1
USE_JWT_EXPIRE=true
JWT_EXPIRE_SEC=3600
JWT_PRIVATE_PEM=[your private PEM here]
JWT_PUBLIC_PEM=[your public PEM here]
```

| Key              | Description                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| DATABASE_URL     | The SQL database connection URI                                          |
| FRONTEND_URL     | The accepted URL for CORS (* means accept all)                           |
| GUNICORN_WORKERS | How many workers you want for gunicorn                                   |
| GUNICORN_THREADS | How many threads you want for gunicorn                                   |
| USE_JWT_EXPIRE   | If true, JWT tokens will expire in JWT_EXPIRE_SEC seconds after creation |
| JWT_EXPIRE_SEC   | Time, in seconds, for the JWT tokens to expire                           |
| JWT_PRIVATE_PEM  | RSA private key for JWT signing                                          |
| JWT_PUBLIC_PEM   | RSA public key to verify JWT signature                                   |

#### Setting manually on Dockerfile
For this, you can modify the ``pytasks/api/Dockerfile`` file and configure your env variables in the format ``ENV KEY=VALUE``.

For example:

```Dockerfile title="api/Dockerfile"
FROM python:3.10-slim-bullseye
COPY . /app
ENV DATABASE_URL=postgres://user:password@ip:5432/pytasks
ENV AMQP_URL=amqp://user:password@ip:5672
ENV FRONTEND_URL=*
ENV GUNICORN_WORKERS=3
ENV GUNICORN_THREADS=1
ENV USE_JWT_EXPIRE=true
ENV JWT_EXPIRE_SEC=3600
ENV JWT_PRIVATE_PEM=[your private PEM here]
ENV JWT_PUBLIC_PEM=[your public PEM here]
EXPOSE 8080
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN python /app/tasks/manager/manager.py -i physicsjs test --api /app
WORKDIR /app
ENTRYPOINT gunicorn --conf /app/gunicorn.conf.py app:app
```
#### Setting manually on docker-compose.yml
For this, you can modify the ``pytasks/docker-compose.yml`` file and configure your env variables in the API service declaration.

For example:

```yaml
services:
  api:
    image: brenopelegrin/pytasks-api:latest
    ports:
      - "8080:8080"
    networks:
      - pytasks-network
    environment:
        - DATABASE_URL: postgres://user:password@ip:5432/pytasks
        - AMQP_URL: amqp://user:password@ip:5672
        - FRONTEND_URL: *
        - GUNICORN_WORKERS: 3
        - GUNICORN_THREADS: 1
        - USE_JWT_EXPIRE: true
        - JWT_EXPIRE_SEC: 3600
        - JWT_PRIVATE_PEM: 'your private PEM here'
        - JWT_PUBLIC_PEM: 'your public PEM here'
```

## Configuring ``handler``


