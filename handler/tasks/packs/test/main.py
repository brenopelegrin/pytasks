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
        from tasks.packs.test.resources import example_resource as myResource
        return(myResource.hypot(x, y))

    @authorized_task
    @celery_app.task
    def myProtectedTask(x: int, y: int):
        return x+y
