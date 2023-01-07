from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from celery import Celery
import time as time
import os

database_url=os.getenv('DATABASE_URL').replace('postgres', 'postgresql', 1)
amqp_url=os.getenv('AMQP_URL')
app = Celery('tasks', backend='db+'+database_url, broker=amqp_url)
app.conf.task_default_queue = 'tasks'
app.config_from_object('celeryconfig')

@app.task
def add(x: int, y: int):
    return x + y

from resources import mov3d as mov3d_module

@app.task
def mov3d(dt: float, r0: list, v0: list, mass: float, radius: float, drag: bool):
    body = mov3d_module.SphericalBody(mass=mass, radius=radius, drag_coefficient=0.5)
    fluid = mov3d_module.Fluid(density=1.184, knematic_viscosity=15.52e-6)

    sim = mov3d_module.Simulation3D(body_params=body.params, fluid_params=fluid.params, r0=r0, v0=v0, dt=dt)
    sim.config["drag"] = drag
    sim.run()

    result = sim.result
    return result

@app.task
def myProtectedTask(x: int, y: int)
    return x+y
