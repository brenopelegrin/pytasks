def init(celery_app):
    from glob import glob
    import os
    paths = glob('./tasks/packs/*')
    availablePackages = []
    for path in paths:
        if os.path.isdir(path) and '__pycache__' not in path:
            packageName = path.replace('./tasks/packs/', '')

            if(not os.path.isfile(path+'/installed.lock')):
                print(f"[package] package '{packageName}' doesn't have 'installed.lock' file -> ignoring the package.")
            else:
                print(f"[package] package '{packageName}' has 'installed.lock' file -> loading the package.")
                if(packageName not in availablePackages):
                    availablePackages.append(packageName)
                else:
                    printf(f"[package] there is already a package named {moduleName}, package name must be unique -> only the first package named '{moduleName}' will be loaded")
    
    for package in availablePackages:
        exec(f"import tasks.packs.{package} as {package}")
        exec(f"{package}.init(celery_app)")