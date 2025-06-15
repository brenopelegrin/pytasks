from glob import glob
import os
import logging

def init(celery_app, **global_decorators):
    logger = logging.getLogger()
    paths = glob('./tasks/packs/*')
    available_packages = []
    for path in paths:
        if os.path.isdir(path) and '__pycache__' not in path:
            package_name = path.replace('./tasks/packs/', '')

            if(not os.path.isfile(path+'/installed.lock')):
                logger.warning(f"[package] package '{package_name}' doesn't have 'installed.lock' file -> ignoring the package.")
            else:
                logger.info(f"[package] package '{package_name}' has 'installed.lock' file -> loading the package.")
                if(package_name not in available_packages):
                    available_packages.append(package_name)
                else:
                    logger.info(f"[package] there is already a package named {package_name}, package name must be unique -> only the first package named '{package_name}' will be loaded")
    
    for package in available_packages:
        exec(f"import tasks.packs.{package} as {package}")
        exec(f"{package}.init(celery_app, **global_decorators)")