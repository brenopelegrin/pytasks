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
For this, you can modify the ``api.env`` file and configure your env variables in the format ``KEY=VALUE``.
#### Setting manually on Dockerfile
#### Setting manually on docker-compose.yml

## Configuring ``handler``


