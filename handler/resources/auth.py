class AuthorizedTasks:
    def __init__(self):
        self.list = {}
        self.auth_data = {}
    def register_task(self, func):
        self.list[func.__name__]={"func": func}
        self.auth_data[func.__name__]={"func": func}

authorizedTasks = AuthorizedTasks()

def authorized_task(task_func):
    if task_func not in authorizedTasks.list:
        print(f"task {task_func.__name__} is authorized")
        authorizedTasks.register_task(task_func)
    def wrapper(*args, **kwargs):
        return task_func(*args, **kwargs)
    return wrapper