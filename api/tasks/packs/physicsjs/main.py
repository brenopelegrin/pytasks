def init(celery_app, **global_decorators):
    @celery_app.task
    def mov3d(dt: float, r0: list, v0: list, mass: float, radius: float, drag: bool):
        from tasks.packs.physicsjs.resources import mov3d as mov3d_module
        body = mov3d_module.SphericalBody(mass=mass, radius=radius, drag_coefficient=0.5)
        fluid = mov3d_module.Fluid(density=1.184, knematic_viscosity=15.52e-6)

        sim = mov3d_module.Simulation3D(body_params=body.params, fluid_params=fluid.params, r0=r0, v0=v0, dt=dt)
        sim.config["drag"] = drag
        sim.run()

        result = sim.result
        return result