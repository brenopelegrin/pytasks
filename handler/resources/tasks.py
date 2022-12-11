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
    return x+y


from resources.tasks_res import mov3d as mov3d_module

@task
def mov3d(dt: float, r0: list, v0: list, mass: float, radius: float, drag: bool):
    body = mov3d_module.SphericalBody(mass=mass, radius=radius, drag_coefficient=0.5)
    fluid = mov3d_module.Fluid(density=1.184, knematic_viscosity=15.52e-6)

    sim = mov3d_module.Simulation3D(body_params=body.params, fluid_params=fluid.params, r0=r0, v0=v0, dt=dt)
    sim.config["drag"] = drag
    sim.run()

    result = sim.result
    return result