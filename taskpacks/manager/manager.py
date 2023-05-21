from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from rich.console import Console
import argparse 
import os
import json

officialPackagesUrl = 'https://raw.githubusercontent.com/brenopelegrin/pytasks/master/taskpacks/official/packages.json'

def install(packages, context, console):
    """_summary_

    Args:
        packages (_type_): _description_
        context (_type_): _description_
        console (_type_): _description_
    """
    if(packages != []):
        console.print("[bold white]Installing the following packages: ")
        [console.print(f"\t[italic green](+) {x}") for x in packages]
        if(context['handler']['dir']):
            installDependencies = False
            extractedPackages = []
            handlerDir = ""
            for package in packages:
                if(package in context["officialPackagesManifest"]):
                    console.print(f"[bold white](wheel/handler/install) donwloading package [bold green]'{package}'")
                    packageUrl = context["officialPackagesManifest"][package]['link']
                    handlerDir = context['handler']['dir']
                    if(os.path.isdir(handlerDir)):
                        os.chdir(handlerDir)
                        packageInstallDir = os.path.join(handlerDir, f'tasks/packs/{package}')
                        if(os.path.isdir(packageInstallDir)):
                            os.system(f'rm -rf {packageInstallDir}')
                        else:
                            os.mkdir(packageInstallDir)
                        if package not in extractedPackages:
                            with urlopen(packageUrl) as zipresp:
                                console.print(f"[bold white](wheel/handler/install) extracting package [bold green]'{package}'")
                                with ZipFile(BytesIO(zipresp.read())) as zfile:
                                    zip_parent_dir = zfile.infolist()[0].filename
                                    zip_infos = zfile.infolist()
                                    zip_infos.pop(0)
                                    for zip_info in zip_infos:
                                        zip_info.filename = zip_info.filename.replace(zip_parent_dir, '')
                                        zfile.extract(zip_info, path=packageInstallDir)
                                    console.print(f"[bold white](wheel/handler/install) extracted package [bold green]'{package}'")
                                    extractedPackages.append(package)
                        installDependencies = True
                else:
                    console.print(f"[bold red]:warning: (wheel/handler/install) package '{package}' not found on official packages manifest.")

            console.print(f"[bold white](wheel/handler/install) installing dependencies for extracted packages [bold green]{extractedPackages}\n")
            os.chdir(handlerDir)
            if(os.path.isfile(os.path.join(handlerDir, 'tasks/install_packs.py'))):
                os.system('python tasks/install_packs.py')
                console.print(f"\n[bold white](wheel/handler/install) installed dependencies for extracted packages [bold green]{extractedPackages}")
            else:
                console.print(f"\n[bold red]:warning: (wheel/handler/install) couldn't install dependencies for extracted packages [bold green]{extractedPackages}: [bold white] install_packs.py not found on handler/tasks/packs.")
            console.print(f"\n[bold white](wheel/handler/install) finished.\n")
        else:
            console.print(":warning: (wheel/handler/install) Argument --handler was not passed. No changes will be made on handler directory.")
        if(context['api']['dir']):
            installDependencies = False
            extractedPackages = []
            apiDir = ""
            for package in packages:
                if(package in context["officialPackagesManifest"]):
                    console.print(f"[bold white](wheel/api/install) donwloading package [bold green]'{package}'")
                    packageUrl = context["officialPackagesManifest"][package]['link']
                    apiDir = context['api']['dir']
                    if(os.path.isdir(apiDir)):
                        os.chdir(apiDir)
                        packageInstallDir = os.path.join(apiDir, f'tasks/packs/{package}')
                        if(os.path.isdir(packageInstallDir)):
                            os.system(f'rm -rf {packageInstallDir}')
                        else:
                            os.mkdir(packageInstallDir)
                        if package not in extractedPackages:
                            with urlopen(packageUrl) as zipresp:
                                console.print(f"[bold white](wheel/api/install) extracting package [bold green]'{package}'")
                                with ZipFile(BytesIO(zipresp.read())) as zfile:
                                    zip_parent_dir = zfile.infolist()[0].filename
                                    zip_infos = zfile.infolist()
                                    zip_infos.pop(0)
                                    for zip_info in zip_infos:
                                        zip_info.filename = zip_info.filename.replace(zip_parent_dir, '')
                                        zfile.extract(zip_info, path=packageInstallDir)
                                    console.print(f"[bold white](wheel/api/install) extracted package [bold green]'{package}'")
                                    extractedPackages.append(package)
                        installDependencies = True
                else:
                    console.print(f"[bold red]:warning: (wheel/api/install) package '{package}' not found on official packages manifest.")

            console.print(f"[bold white](wheel/api/install) installing dependencies for extracted packages [bold green]{extractedPackages}\n")
            os.chdir(apiDir)
            if(os.path.isfile(os.path.join(apiDir, 'tasks/install_packs.py'))):
                os.system('python tasks/install_packs.py')
                console.print(f"\n[bold white](wheel/api/install) installed dependencies for extracted packages [bold green]{extractedPackages}")
            else:
                console.print(f"\n[bold red]:warning: (wheel/api/install) couldn't install dependencies for extracted packages [bold green]{extractedPackages}: [bold white] install_packs.py not found on api/tasks/packs.")
            console.print(f"\n[bold white](wheel/api/install) finished.\n")
        else:
            console.print(":warning: (wheel/api/install) Argument --api was not passed. No changes will be made on api directory.")
    return

if __name__ == '__main__':
    console = Console()
    envInstallPackages = os.getenv('pytasks.taskpacks.manager.INSTALL_PACKAGES') 
    parser = argparse.ArgumentParser(
        prog="manager",
        description="package manager for flask-tasks-docker")
    parser.add_argument('-i', '--install', dest='installs', nargs='+',
        help="Install packages passed after argument. Example: -i package1 package2 package3")
    parser.add_argument('-handler', '--handler', dest='handler_dir',
        help="Specify the directory where the handler folder is located. If not specified, no changes will be made on handler.")
    parser.add_argument('-api', '--api', dest='api_dir',
        help="Specify the directory where the api folder is located. If not specified, no changes will be made on api.")
    parser.add_argument('-pl', '--packagelist', dest='custom_package_list', action='store',
        help="Use a custom package list manifest to fetch the available packages for installation. Example: -pl https://raw.myrepo.com/packages.json")
    args = parser.parse_args()
    
    if(envInstallPackages != None):
        listOfPackages = envInstallPackages.split(",")
        toBeInstalled = []
        console.print(f"[yellow](manager) Detected env variable with installs [bold yellow](pytasks.taskpacks.manager.INSTALL_PACKAGES)[yellow] containing the following packages: {listOfPackages}")
        for package in listOfPackages:
            if package not in args.installs:
                toBeInstalled.append(package)
                args.installs.append(package)
        console.print(f"[yellow](manager) Pakcages from [bold yellow](pytasks.taskpacks.manager.INSTALL_PACKAGES)[yellow] env variable added to installs list: {toBeInstalled}")
                
    currentContext = {
        "officialPackagesManifest": {} ,
        "handler":{
            "dir": args.handler_dir,
        },
        "api":{
            "dir": args.api_dir,
        }
    }

    if(args.custom_package_list):
        try:
            currentContext["officialPackagesManifest"] = json.loads(urlopen(args.custom_package_list).read())
        except:
            console.print(f"[bold red]:warning: Can't reach custom package list manifest at [bold white]'{args.custom_package_list}'.[bold red] Exiting.")
            exit()
    else:
        try:
            currentContext["officialPackagesManifest"] = json.loads(urlopen(officialPackagesUrl).read())
        except:
            console.print(f"[bold red]:warning: Can't reach official package list manifest at [bold white]'{officialPackagesUrl}'.[bold red] Exiting.")
            exit()


    console.print("> Welcome to [bold blue]taskpacks-manager! [white italic]@flask-tasks-docker/release/3")
    if(args.installs):
        install(packages=args.installs, context=currentContext, console=console)
    else:
        console.print("[italic white]No packages passed on -i or --install. No changes will be made. Exiting.")
        exit()
