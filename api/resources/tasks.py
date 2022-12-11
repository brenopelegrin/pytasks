import inspect

class Tasks:
    def __init__(self):
        self.list = {}
    def register_task(self, func):
        annotations = inspect.getfullargspec(func).annotations
        if annotations != {}:
            self.list[func.__name__]={"func": func, "args": annotations}
        else:
            raise NameError(f"arguments of function {func.__name__} not found.")

tasks = Tasks()

def task(task_func):
    if task_func not in tasks.list:
        tasks.register_task(task_func)
    def wrapper(*args, **kwargs):
        return task_func(*args, **kwargs)
    return wrapper

@task
def add(x: int, y: int):
    return None

@task
def mov3d(dt: float, r0: list, v0: list, mass: float, radius: float, drag: bool):
    return None