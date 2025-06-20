import os
import sys
import json
import argparse 
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

from rich.console import Console

official_packages_url = 'https://raw.githubusercontent.com/brenopelegrin/pytasks/deploy-soicmc/taskpacks/official/packages.json'

def install(packages, context, console):
    """_summary_

    Args:
        packages (_type_): _description_
        context (_type_): _description_
        console (_type_): _description_
    """
    if packages:
        console.print("[bold white]Installing the following packages: ")
        for p in packages:
            console.print(f"\t[italic green](+) {p}")
            
        if context['handler']['dir']:
            # Handles the download/extract/installation for handler packages
            install_dependencies = False
            extracted_packages = []
            handler_dir = ""
            
            for package in packages:
                # If package is found on official packages repository manifest, download and extract it
                if package in context["official_packages_manifest"]:
                    console.print(f"[bold white](wheel/handler/install) donwloading package [bold green]'{package}'")
                    package_url = context["official_packages_manifest"][package]['link']
                    handler_dir = context['handler']['dir']
                    
                    # Extracts the downloaded package
                    if os.path.isdir(handler_dir):
                        os.chdir(handler_dir)
                        package_install_dir = os.path.join(handler_dir, f'tasks/packs/{package}')
                        if os.path.isdir(package_install_dir):
                            os.system(f'rm -rf {package_install_dir}')
                        else:
                            os.mkdir(package_install_dir)
                        if package not in extracted_packages:
                            with urlopen(package_url) as zipresp:
                                console.print(f"[bold white](wheel/handler/install) extracting package [bold green]'{package}'")
                                with ZipFile(BytesIO(zipresp.read())) as zfile:
                                    zip_parent_dir = zfile.infolist()[0].filename
                                    zip_infos = zfile.infolist()
                                    zip_infos.pop(0)
                                    for zip_info in zip_infos:
                                        zip_info.filename = zip_info.filename.replace(zip_parent_dir, '')
                                        zfile.extract(zip_info, path=package_install_dir)
                                    console.print(f"[bold white](wheel/handler/install) extracted package [bold green]'{package}'")
                                    extracted_packages.append(package)
                        install_dependencies = True
                else:
                    console.print(f"[bold red]:warning: (wheel/handler/install) package '{package}' not found on official packages manifest.")

            console.print(f"[bold white](wheel/handler/install) installing dependencies for extracted packages [bold green]{extracted_packages}\n")
            
            # Runs the install_packs script
            os.chdir(handler_dir)
            if(os.path.isfile(os.path.join(handler_dir, 'tasks/install_packs.py'))):
                os.system('python tasks/install_packs.py')
                console.print(f"\n[bold white](wheel/handler/install) installed dependencies for extracted packages [bold green]{extracted_packages}")
            else:
                console.print(f"\n[bold red]:warning: (wheel/handler/install) couldn't install dependencies for extracted packages [bold green]{extracted_packages}: [bold white] install_packs.py not found on handler/tasks/packs.")
            console.print("\n[bold white](wheel/handler/install) finished.\n")
        else:
            console.print(":warning: (wheel/handler/install) Argument --handler was not passed. No changes will be made on handler directory.")
        
        if context['api']['dir']:
            install_dependencies = False
            extracted_packages = []
            api_dir = ""
            
            for package in packages:
                if package in context["official_packages_manifest"]:
                    # If package is found on official packages repository manifest, download and extract it
                    console.print(f"[bold white](wheel/api/install) donwloading package [bold green]'{package}'")
                    package_url = context["official_packages_manifest"][package]['link']
                    api_dir = context['api']['dir']
                    
                    # Extracts the downloaded package
                    if os.path.isdir(api_dir):
                        os.chdir(api_dir)
                        package_install_dir = os.path.join(api_dir, f'tasks/packs/{package}')
                        if os.path.isdir(package_install_dir) :
                            os.system(f'rm -rf {package_install_dir}')
                        else:
                            os.mkdir(package_install_dir)
                        if package not in extracted_packages:
                            with urlopen(package_url) as zipresp:
                                console.print(f"[bold white](wheel/api/install) extracting package [bold green]'{package}'")
                                with ZipFile(BytesIO(zipresp.read())) as zfile:
                                    zip_parent_dir = zfile.infolist()[0].filename
                                    zip_infos = zfile.infolist()
                                    zip_infos.pop(0)
                                    for zip_info in zip_infos:
                                        zip_info.filename = zip_info.filename.replace(zip_parent_dir, '')
                                        zfile.extract(zip_info, path=package_install_dir)
                                    console.print(f"[bold white](wheel/api/install) extracted package [bold green]'{package}'")
                                    extracted_packages.append(package)
                        install_dependencies = True
                else:
                    console.print(f"[bold red]:warning: (wheel/api/install) package '{package}' not found on official packages manifest.")

            console.print(f"[bold white](wheel/api/install) installing dependencies for extracted packages [bold green]{extracted_packages}\n")
            
            # Runs the install_packs script
            os.chdir(api_dir)
            if os.path.isfile(os.path.join(api_dir, 'tasks/install_packs.py')):
                os.system('python tasks/install_packs.py')
                console.print(f"\n[bold white](wheel/api/install) installed dependencies for extracted packages [bold green]{extracted_packages}")
            else:
                console.print(f"\n[bold red]:warning: (wheel/api/install) couldn't install dependencies for extracted packages [bold green]{extracted_packages}: [bold white] install_packs.py not found on api/tasks/packs.")
            console.print("\n[bold white](wheel/api/install) finished.\n")
        else:
            console.print(":warning: (wheel/api/install) Argument --api was not passed. No changes will be made on api directory.")
    return

if __name__ == '__main__':
    console = Console()
    env_install_packages = os.getenv('pytasks_taskpacks_manager_INSTALL_PACKAGES') 
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
    
    if env_install_packages is not None:
        if('*' in env_install_packages):
            console.print("[yellow]:warning: (manager) Detected [yellow bold]WILDCARD on env variable pytasks_taskpacks_manager_INSTALL_PACKAGES.[yellow] ALL command-line installs will be ignored and only env variable installs will be considered.")
            args.installs = []
            env_install_packages = env_install_packages.replace('*', '')

        list_of_packages = env_install_packages.split(",")

        to_be_installed = []
        console.print(f"[yellow](manager) Detected env variable with installs [bold yellow](pytasks_taskpacks_manager_INSTALL_PACKAGES)[yellow] containing the following packages: {list_of_packages}")
        for package in list_of_packages:
            if package not in args.installs:
                to_be_installed.append(package)
                args.installs.append(package)
        console.print(f"[yellow](manager) Pakcages from [bold yellow](pytasks_taskpacks_manager_INSTALL_PACKAGES)[yellow] env variable added to installs list: {to_be_installed}")
                
    current_context = {
        "official_packages_manifest": {} ,
        "handler":{
            "dir": args.handler_dir,
        },
        "api":{
            "dir": args.api_dir,
        }
    }

    if(args.custom_package_list):
        try:
            current_context["official_packages_manifest"] = json.loads(urlopen(args.custom_package_list).read())
        except BaseException:
            console.print("[bold red]:warning: Can't reach custom package list manifest at [bold white]'{args.custom_package_list}'.[bold red] Exiting.")
            sys.exit()
    else:
        try:
            current_context["official_packages_manifest"] = json.loads(urlopen(official_packages_url).read())
        except BaseException:
            console.print("[bold red]:warning: Can't reach official package list manifest at [bold white]'{official_packages_url}'.[bold red] Exiting.")
            sys.exit()


    console.print("> Welcome to [bold blue]taskpacks-manager! [white italic]@flask-tasks-docker/release/3")
    if(args.installs):
        install(packages=args.installs, context=current_context, console=console)
    else:
        console.print("[italic white]No packages passed on -i or --install. No changes will be made. Exiting.")
        sys.exit()
