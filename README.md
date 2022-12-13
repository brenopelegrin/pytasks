# flask-tasks-docker

This is a generic ready-to-run Flask RESTful API written in Python that can receive task requests with some arguments, run some logic with the arguments provided and store the results on a SQL database. The results can then be retrieved from the API. The processing instances can be scaled according to your needs using docker.

⏳ **Upcoming in v2.0**: the app will be redesigned to manage the tasks using **Celery + RabbitMQ + PostgreSQL**

## Main features

- You can scale multiple task handlers that can **proccess tasks in parallel**
- **Highly customizable** to fulfill your needs
- You can scale multiple janitors that can clean up the database in parallel
- Can receive task from ```POST``` request **passing multiple parameters** in ```json```
- Can store the received tasks in a SQL database and **do some computation** with them
- Can return the result of the task from ```GET``` request passing the task ID as parameter


## :rocket: Getting started

- In what applications should I use it?
  
    You should use the ```flask-tasks``` when you need a server to do some computation based on received arguments and store the results of the computation for later visualization

### :gear: Setting up and running

First, make sure you have ```docker```and ```docker compose``` installed.

Then, clone the repository and go to the cloned directory:
```bash
git clone https://github.com/brenopelegrin/flask-tasks-docker.git && cd flask-tasks-docker
```

:warning: Before building, please **make sure to configure the environment variables**.

Then, run the docker compose build command
```bash
docker compose build --no-cache --pull
```

Then, run the docker compose up command and specify how many handler and janitor instances you want
```bash
docker compose up --scale janitor=1 --scale handler=1
```

### Configuring environment variables
Before running the docker compose, you need to configure the environment variables for each service (postgres, api, handler, janitor) in the ```docker-compose.yml``` file. 

Below, you have an example of the environment variables for ```api```. Copy the same variables for the other services.

```yaml
services:
  api:
    environment:
      - DATABASE_URL: "postgres://[user]:[password]@[database_server_ip]:[port]/[database_name]"
      - BACKEND_URL: "https://[backend_server_ip]:[port]"
      - FRONTEND_URL: "https://[frontend_server_ip]:[port]"
      - MAX_TASK_TIME: "[time_in_seconds]"
```
If you want your frontend app to connect with the API, then fill the ```FRONTEND_URL``` and ```BACKEND_URL``` for the JavaScript CORS to work.

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
"id": 192,
"result": null,
"args": {"x": 1, "y": 2},
"status": "waiting",
"expire": 1668797956,
"type": "add",
"created": 1668797946
}
```

If the task type passed doesn't match the name of any function declared in the ```api/resources/tasks.py``` file, then it will return an error:

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
"id": 204,
"result": {[all results of simulation]},
"args": {[args you passed]},
"status": "done",
"expire": 1668797956,
"type": "mov3d",
"created": 1668797946
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
curl -X GET localhost:5000/task/1/view
```

Example of response:

```json
{
"id": 192,
"result": {"message": 3},
"args": {"x": 1, "y": 2},
"status": "done",
"expire": 1668797956,
"type": "add",
"created": 1668797946
}
```

The status of a retrieved task can be:
- ```waiting```
  
  Means that the task has been registered but has not yet been computed
- ```running```
  
  Means that the task has been registered and is actually being computed
- ```done```
  
  Means that the task has been registered and have already been computed

## The ```handler```

The handler is a module of the system that will scan through the database and get the tasks with ```waiting``` status.

If the found task has a type which matches the name of some function defined in the ```handler/resources/tasks.py``` file, then it will execute the function, passing the task arguments. After that, the result is stored in the ```result``` key of the task in the database.

You can add as many tasks as you want in the code, by adding the decorator ```@tasks``` on top of a function in the ```resources\tasks.py``` file. Then, the function name will become a new task type and can be called from the API. For example, if you want to add a task that adds two numbers x and y, you should write the following:

```python
@task
def add(x:int, y:int):
  return x+y
```

It is required to ***explicitly declare the function arguments with annotations*** so that the API can process them correctly.

The handler will mark the current task row as locked in the database, so that the other instances of handlers can't edit at the same time.


>***⚠️ In order for all tasks processed by the API to be able to run on all handler instances, both the API and Handler ```resources/tasks.py``` file must be EXACTLY the same***. 

> If you want some handler instances to run only specific tasks, see the ```Customizing handler instances for specific tasks``` section.


## The ```janitor```
The janitor is a module of the system that will scan through the database and get the tasks that exceeded the maximum data permanency time (```MAX_TASK_TIME``` variable) in the database.

Then, it will delete the task from the database. The janitor will mark the current task row as locked in the database, so that the other instances of handlers can't edit at the same time. 

## Customizing handler instances for specific tasks
A handler instance will only run the tasks that have been declared on the ```handler/resources/tasks.py```. 

If you want some tasks to run in a specific handler instance, then you should copy the source ```handler``` directory to directories with different names for each handler instance type you want:

```bash
mkdir handler-type1
mkdir handler-type2
cp -r handler handler-type1
cp -r handler handler-type2
```

Then, you can edit each ```handler-typeX/resources/tasks.py``` file and add specific tasks to each handler.

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
  janitor:
    build: ./janitor
    network_mode: "host"
    environment:
      DATABASE_URL: "postgres://postgres:123@localhost:5432/flask_tasks"
  handler-type1:
    build: ./handler-type1
    network_mode: "host"
    environment:
      DATABASE_URL: "postgres://postgres:123@localhost:5432/flask_tasks"
  handler-type2:
    build: ./handler-type1
    network_mode: "host"
    environment:
      DATABASE_URL: "postgres://postgres:123@localhost:5432/flask_tasks"
```

To deploy, run the docker compose build command
```bash
docker compose build --no-cache --pull
```

Then, run the docker compose up command and specify how many ```handler-typeX``` and janitor instances you want

```bash
docker compose up --scale janitor=1 --scale handler-type1=1 --scale handler-type2=1
```
