# flask-tasks-docker

This is a generic ready-to-run Flask RESTful API written in Python that can receive task requests with some arguments, run some logic with the arguments provided (using Celery and AMQP queues) and store the results on a SQL database. The results can then be retrieved from the API. The processing instances can be scaled according to your needs using docker.

## Main features

- You can scale multiple workers that can **proccess tasks in parallel**
- You can add as many **custom tasks** as you want: highly customizable
- Can receive tasks from ```POST``` requests **passing multiple parameters** in ```json```
- Can store the result of the tasks in a SQL database
- Can return the result of a task from ```GET``` requests passing the task ID as parameter

## :rocket: Getting started

- In what applications should I use it?
  
    You should use the ```flask-tasks``` when you need a server to do some computation based on received arguments and store the results of the computation for later visualization

### :gear: Setting up and running

First, make sure you have ```docker```and ```docker compose``` installed.

:warning: Before running, please **make sure to configure the environment variables for API and Handler**.

To run the API docker container, use the following command.
```bash
docker run --network=host brenopelegrin/flask-tasks-api:latest
```

To run the worker container, use the following command. You will need to have ```uuidgen``` to generate a unique worker name.

```bash
docker run --network=host --env WORKER_NAME=`uuidgen` brenopelegrin/flask-tasks-handler:latest
```

If you want to specify a custom worker name, change the ```WORKER_NAME``` variable. Make sure that all workers have unique names.


### Configuring environment variables

- API:
  
  Please set the SQL Database URL, the AMQP backend URL, and the number of gunicorn workers and threads you want. 

  If you want to, you can allow CORS only for your front-end site by setting the FRONTEND_URL with the front-end URL.

  You need to generate a 256 RSA keypair to use authentication based on JWT tokens.

  ```Dockerfile
  ENV DATABASE_URL postgres://postgres:123@localhost:5432/flask_tasks_v2
  ENV AMQP_URL redis://localhost:6379
  ENV FRONTEND_URL *
  ENV GUNICORN_WORKERS 3
  ENV GUNICORN_THREADS 1
  ENV JWT_PUBLIC_PEM "<Your public RSA 256 key here>"
  ENV JWT_PRIVATE_PEM "<Your public RSA 256 key here>"
  ```

  To generate the 256 RSA keypar, you can run the following (make sure to have openssl installed):

  ```
  openssl genrsa -out private.pem 2048 && openssl rsa -in private.pem -pubout -out public.pem
  ```

  Then, set the environment variables with your keys.

- Handler:
  
  Please set the SQL Database URL, the AMQP backend URL and the worker name you want. Make sure the worker name is unique.

  ```Dockerfile
  ENV DATABASE_URL postgres://postgres:123@localhost:5432/flask_tasks_v2
  ENV AMQP_URL redis://localhost:6379
  ENV WORKER_NAME worker
  ```
  
## API endpoints

### /task/new

Method: ```POST```

This endpoint will register a new task in the server. You need to pass some required arguments inside a ```application/json```. The json should contain a string with the task type, named ```type``` and the task-specific required arguments as a dictionary, named ```args```:

Example of request (task of type "add"):

Parameters:
```json
{
    "type":"add",
    "args": {
      "x": 1,
      "y": 2
    }
}
```

```bash
curl -X POST localhost:5000/task/new -H 'Content-Type: application/json' -d '{"type":"add", "args":{"x": 1, "y": 2}}'
```

Example of response:

```json
{
  "id": "5861c3a8-fa0f-4b84-9e54-04b545408114",
  "result": {},
  "args": {"x": 1, "y": 2},
  "status": "PENDING",
  "type": "add",
}
```

If the task type passed doesn't match the name of any function declared in the ```api/tasks.py``` file, then it will return an error:

```json
{
  "message":"task type [tasktype] doesnt exist"
}
```

If the task exists but you didn't pass an required argument of the declared function, then it will return an error:

```json
{
  "message": "the required param [param] was not passed."
}
```

If the task exists, all arguments were passed but the type of an argument doesn't match the type of the argument on the declared function, then it will return an error:

```json
{
  "message": "the passed param [param] doesnt match the required type: [required type]."
}
```

If you pass an argument that is not required, then it will return an error:

```json
{
   "message": "the passed param [param] is not required."
}
```

You can also use the example task "mov3d" for testing purposes, which will simulate the trajectory of a particle:

Parameters:
```json
{
    "type":"mov3d",
    "args": {
      "dt": 0.001,
      "mass": 1.0,
      "r0": [0.5, 0.5, 0.5],
      "v0": [10.0, 10.0, 10.0],
      "radius": 0.3,
      "drag": false
    }
}
```

Example of response:

```json
{
  "id": "5861c348-fa0f-4b84-9e54-04b545408114",
  "result": {[all results of simulation]},
  "args": {[args you passed]},
  "status": "SUCCESS",
  "type": "mov3d",
}
```
Where the "result" will contain the following:
```json
"result": 
{
    "r": [[x1,y1,z1], [x2,y2,z2], [xn,yn,zn]],
    "v": [[x1,y1,z1], [x2,y2,z2], [xn,yn,zn]],
    "a": [[x1,y1,z1], [x2,y2,z2], [xn,yn,zn]],
    "alpha": [[x1,y1,z1], [x2,y2,z2], [xn,yn,zn]],
    "w": [[x1,y1,z1], [x2,y2,z2], [xn,yn,zn]],
    "t": [t1, t2, tn]
}
```

### /task/```<task_id>```/view

Method: ```GET```

This endpoint will return the current data for the task with id ```task_id``` in ```application/json``` format:

Example of request:

Parameters: ```<task_id>```

```bash
curl -X GET localhost:5000/task/5861c3a8-fa0f-4b84-9e54-04b545408114/view
```

Example of response:

```json
{
  "id": "5861c3a8-fa0f-4b84-9e54-04b545408114",
  "result": 3,
  "args": {"x": 1, "y": 2},
  "status": "SUCCESS",
  "type": "add",
}
```

The status of a retrieved task can be:
- ```PENDING```
  
  Means that the task doesn't exist *OR* exists and has not yet been received by a worker.

- ```STARTED```
  
  Means that the task has been received by a worker and is actually being computed

- ```SUCCESS```
  
  Means that the task has been received by a worker, have already been computed and is available for view

## The ```handler```

The handler is a module of the system based on Celery that will subscribe to the AMQP queue and wait for new tasks. When it receives a task, it will execute the task and store its value on the SQL database. 

You can add as many tasks as you want in the code, by adding the decorator ```@app.task``` on top of a function in the ```handler\tasks.py``` file. Then, the function name will become a new task type and can be called from the API. For example, if you want to add a task that adds two numbers x and y, you should write the following:

```python
@app.tasks
def add(x:int, y:int):
  return x+y
```

It is required to ***explicitly declare the function arguments with annotations*** so that the API can process them correctly.

The handler will mark the current task row as locked in the database, so that the other instances of handlers can't edit at the same time.


>***⚠️ In order for all tasks processed by the API to be able to run on all handler instances, both the API and Handler ```tasks.py``` file must be EXACTLY the same***. 

> If you want some handler instances to run only specific tasks, see the ```Customizing handler instances for specific tasks``` section.

## Customizing handler instances for specific tasks
A handler instance will only run the tasks that have been declared on the ```handler/tasks.py```. 

If you want some tasks to run in a specific handler instance, then you should copy the source ```handler``` directory to directories with different names for each handler instance type you want:

```bash
mkdir handler-type1
mkdir handler-type2
cp -r handler handler-type1
cp -r handler handler-type2
```

Then, you can edit each ```handler-typeX/tasks.py``` file and add specific tasks to each handler.

After that, you can customize your ```docker-compose.yml``` file to scale your different handler instance types:

```yaml
version: "3"
services:
  api:
    build: ./api
    ports:
      - "8000:8080"
    network_mode: "host"
    environment:
      DATABASE_URL: "postgres://postgres:123@localhost:5432/flask_tasks" 
  handler-type1:
    build: ./handler-type1
    network_mode: "host"
    environment:
      WORKER_NAME: "worker2"
      AMQP_URL: "redis://localhost:6379"
      DATABASE_URL: "postgres://postgres:123@localhost:5432/flask_tasks"
  handler-type2:
    build: ./handler-type2
    network_mode: "host"
    environment:
      WORKER_NAME: "worker2"
      AMQP_URL: "redis://localhost:6379"
      DATABASE_URL: "postgres://postgres:123@localhost:5432/flask_tasks"
```

To deploy, run the docker compose build command
```bash
docker compose build --no-cache --pull
```

Then, run the docker compose up command:

```bash
docker compose up
```
