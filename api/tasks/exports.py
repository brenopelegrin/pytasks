def init(celery_app, **global_decorators):
    from glob import glob
    import logging
    logger = logging.getLogger('gunicorn.error')
    import os
    paths = glob('./tasks/packs/*')
    availablePackages = []
    for path in paths:
        if os.path.isdir(path) and '__pycache__' not in path:
            packageName = path.replace('./tasks/packs/', '')
            logger.info(f"[package] package '{packageName}' is valid -> loading the package.")
            if(packageName not in availablePackages):
                availablePackages.append(packageName)
            else:
                logger.warning(f"[package] there is already a package named {moduleName}, package name must be unique -> only the first package named '{moduleName}' will be loaded")
    
    for package in availablePackages:
        exec(f"import tasks.packs.{package} as {package}")
        exec(f"{package}.init(celery_app, **global_decorators)")