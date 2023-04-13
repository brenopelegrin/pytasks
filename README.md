![pytasks logo](https://github.com/brenopelegrin/pytasks/blob/master/docs/img/pytasks.png?raw=true)

**pytasks** is a complete and customizable microservice for running computational tasks on remote machines and viewing its results through an API. 

> ⚠  **Notice**: this is only an introduction README. For full documentation, visit the [pytasks documentation page](https://brenopelegrin.github.io/pytasks/).

## Current development

The project is currently on **release 3**.

You can view the [source code](https://github.com/brenopelegrin/pytasks) and contribute by creating a pull request with your modifications or opening an [issue](https://github.com/brenopelegrin/pytasks/issues).

## Getting started

The microservice has two instances, an ``api`` exposed on the web, where users can send task requests to a queue, and a ``handler``, which listens to the queue and execute the tasks.

To run ``pytasks`` with all of its dependencies in a testing environment, ensure you have [docker](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/) installed and then run the following command:

```bash
git clone https://github.com/brenopelegrin/pytasks.git &&
cd pytasks &&
export JWT_PRIVATE_PEM=$(cat ./examples/keys/jwtRS256.key) &&
export JWT_PUBLIC_PEM=$(cat ./examples/keys/jwtRS256.key.pub) &&
docker compose up -d
```

> ⚠ This command uses the example RSA keypair stored in the repository and default passwords for PostgreSQL and RabbitMQ. You **MUST** setup your own RSA keypair and credentials in production to avoid security issues. See the [Setting up](https://brenopelegrin.github.io/pytasks/setup) section for more informations.

After the containers start, the API will be available at ``http://localhost:8080``.

💡  For more instructions on how to customize your ``pytasks`` containers and how to run them, see [Setting up](https://brenopelegrin.github.io/pytasks/setup).
