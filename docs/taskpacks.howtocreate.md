# Creating your own taskpack

Taskpacks are collection of Celery tasks packaged inside a python module with some specifications:

- All tasks functions must be declarated inside the ``init()`` function on the taskpack's ``main.py``.
- All tasks must have annotated arguments: each variable received by the task must have a fixed type (``int``, ``str``, ``float``, others...).
- External resources used by the tasks must be located in Python files inside the taskpack's ``resources`` directory.
- All tasks outputs must be in a ``JSON`` seriallizable format.

## Let's start our project

An example of valid taskpack that you can use as basis is the [pytasks-test](https://github.com/brenopelegrin/pytasks-test) taskpack.
For this guide, we'll be using it as a basis.

First, clone the repository from GitHub and go to its directory:

```bash
git clone https://github.com/brenopelegrin/pytasks-test.git && cd pytasks-test
```

Then, you'll see some files in the parent directory:

| Name             | Description                                                                           |
| ---------------- | ------------------------------------------------------------------------------------- |
| main.py          | Where the ``init()`` function is located. **Declare your tasks inside the function.** |
| \_\_init\_\_.py  | Initialization code used by pytasks to get tasks working. **Do not modify it.**       |
| package.json     | Information about the package: author, name, version, etc.                            |
| requirements.txt | The package dependencies to be installed with pip.                                    |

## Understanding and modifying main.py

The ``main.py`` file contains the following:
```python title="main.py"
def init(celery_app, **global_decorators):
    authorized_task = global_decorators['authorized_task']

    @celery_app.task
    def add(x: int, y: int):
        return x + y
    
    @celery_app.task
    def subtract(x: int, y: int):
        return x-y
    
    @celery_app.task
    def hypot(x: float, y: float):
        from .resources import example_resource as myResource
        return(myResource.hypot(x, y))

    @authorized_task
    @celery_app.task
    def myProtectedTask(x: int, y: int):
        return x+y
```

### Tasks inside main.py

The ``init()`` function receives the ``celery_app`` decorator and ``global_decorators`` from pytasks. By using ``@celery_app.task`` on top of a function, you create a task.
As you can see, every task must have type annotation on its parameters.

:check_mark: Great task with annotations
```python
@celery_app.task
def add(x: int, y: int):
    return x + y
```

:cross_mark: Wrong task without annotations
```python
@celery_app.task
def add(x, y):
    return x + y
```

By default, pytasks passes the ``authorized_task`` decorator inside the ``global_decorators`` object. By using ``@authorized_task`` on top of a **valid task**, pytasks will require authentication for the task to run.

> :warning: Note: for compatibility reasons, you need to declare a variable to unpack the desired decorator inside ``global_decorators``. Do **NOT** use ``@global_decorators['authorized_task']`` directly. See the following example.

To use the ``authorized_task`` decorator, you can do:

```python
def init(celery_app, **global_decorators):
    authorized_task = global_decorators['authorized_task']

    @authorized_task
    @celery_app.task
    def someProtectedTask(user: str, password: str):
        return({"authenticated": True})
```

> :warning: Note: you should **ALWAYS** use global decorators **ON TOP** of ``@celery_app.task``.

## Using external resources inside your tasks

You can put python files inside the ``resources/`` directory. All python files inside this directory can be imported inside your tasks as a module.

For example, see the ``resources/example_resource.py`` file:

```python title="resources/example_resource.py"
def hypot(a, b):
    return(((a**2) + (b**2))**(1/2))
```

This resource is used inside ``main.py``'s ``hypot`` task. See:
```python title="main.py"
def init(celery_app, **global_decorators):

    @celery_app.task
    def hypot(x: float, y: float):
        from .resources import example_resource as myResource
        return(myResource.hypot(x, y))
```

### Best practices for resources:
Taskpacks resources are modules, so you need to follow some best practices for modules:

- Do not declare variables in global scope. Only declare classes and functions.
- Use meaningful names for your functions and classes.
- Do not import other modules inside your resources. Instead, import them directly in the task.

## Modifying package.json

The ``package.json`` file contain information about you and your taskpack. There, you can declare the taskpack version, its author, name, description and license.

For example:

```json title="package.json"
{
    "name": "test",
    "author": "brenopelegrin",
    "version": "1.0",
    "description": "A test package to demonstrate pytasks usage.",
    "license": "MIT"
}

```

## Submitting your taskpack to the official repository

To submit your taskpack to the official pytasks taskpack repository, first push your taskpack directory to a GitHub repository. 

Then, please [open an issue](https://github.com/brenopelegrin/pytasks/issues) on pytasks repository. In your issue, answer the following:

- Taskpack name
- Taskpack short description: main features, purpose and target audience
- All taskpack dependencies
- Taskpack GitHub repository URL 

After some time, your issue will be read and we will decide on including your taskpack in the official repository.