# flask-tasks-docker

This is a generic ready-to-run Flask RESTful API written in Python that can receive task requests with some arguments, run some logic with the arguments provided and store the results on a SQL database. The results can then be retrieved from the API. The processing instances can be scaled according to your needs using docker.

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

This endpoint will register a new task in the server, passing some arguments in ```application/json``` format and returning the task info in ```application/json``` format:

Example of request:

Parameters:
```json
{
    "required_arg":"test"
}
```

```bash
curl -X POST localhost:5000/task/new -H 'Content-Type: application/json' -d '{"required_arg":"test"}'
```

Example of response:

```json
{
"id": 192,
"result": null,
"args": {"required_arg": "test"},
"status": "waiting",
"expire": 1668797956,
"required_arg": "test",
"created": 1668797946
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
"id": 1,
"result": {"message": "some_message"},
"args": {"required_arg": "test"},
"status": "done",
"expire": 1668797956,
"required_arg": "test",
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

Then, it will run the ```ExecuteWhenRunningTask(task_id, args)``` function which should return a result for the task. After that, the result is stored in the ```result``` key of the task in the database. This function can be customized to fulfill your needs.

The handler will mark the current task row as locked in the database, so that the other instances of handlers can't edit at the same time.

## The ```janitor```
The janitor is a module of the system that will scan through the database and get the tasks that exceeded the maximum data permanency time (```MAX_TASK_TIME``` variable) in the database.

Then, it will delete the task from the database. The janitor will mark the current task row as locked in the database, so that the other instances of handlers can't edit at the same time. 
