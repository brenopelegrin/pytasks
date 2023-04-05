def remove(isInteractive, packages, context, console):
    if(packages != []):
        console.print("[bold white]Removing the following packages: ")
        [console.print(f"\t[italic red](-) {x}") for x in packages]
    return

def install(isInteractive, packages, context, console):
    if(packages != []):
        console.print("[bold white]Installing the following packages: ")
        [console.print(f"\t[italic green](+) {x}") for x in packages]
        if(context['handler']['dir']):
            for package in packages:
                console.print(f"[bold white](wheel/handler/install) donwloading package [bold green]{package}")
        else:
            console.print(":warning: (wheel/handler/install) Argument --handler was not passed. No changes will be made on handler.")
        if(context['api']['dir']):
            for package in packages:
                console.print(f"[bold white](wheel) api/install package [bold green]{package}")
        else:
            console.print(":warning: (wheel/api/install) Argument --api was not passed. No changes will be made on api.")
    return

def update(isInteractive, packages, context, console):
    if(packages != []):
        console.print("[bold white]Updating the following packages: ")
        [console.print(f"\t[italic blue](*) {x}") for x in packages]
    return

if __name__ == '__main__':
    from rich.console import Console
    import argparse
    console = Console()

    parser = argparse.ArgumentParser(
        prog="manager",
        description="package manager for flask-tasks-docker")
    parser.add_argument('-interactive', '--interactive', help="Interactive mode", action='store_true')
    parser.add_argument('-i', '--install', dest='installs', nargs='+')
    parser.add_argument('-r', '--remove', dest='removes', nargs='+')
    parser.add_argument('-u', '--update', dest='updates', nargs='+')
    parser.add_argument('-handler', '--handler', dest='handler_dir')
    parser.add_argument('-api', '--api', dest='api_dir')
    args = parser.parse_args()

    currentContext = {
        "handler":{
            "dir": args.handler_dir,
        },
        "api":{
            "dir": args.api_dir,
        }
    }

    isInteractive = args.interactive

    if(not isInteractive):
        if(args.installs):
            install(isInteractive, packages=args.installs, context=currentContext, console=console)
        if(args.removes):
            remove(isInteractive, packages=args.removes, context=currentContext, console=console)
        if(args.updates):
            update(isInteractive, packages=args.updates, context=currentContext, console=console)
        exit()

    console.print("> Welcome to [bold blue]taskpacks-manager! [white italic]@flask-tasks-docker/release/3")
    console.print("|- Please select one of the following options:")
    console.print("\t[bold magenta] r) Remove packages")
    console.print("\t[bold magenta] i) Install packages")
    console.print("\t[bold magenta] u) Update packages")
    console.print("\t[bold red] q) Quit")
    console.print("[bold italic white]> Choice:", end=" ")
    while (operation:=input()) not in ['r', 'i', 'u', 'q']:
        console.print("[bold red]:warning: Invalid operation. \n") 
        console.print("|- Please select one of the following options:")
        console.print("\t[bold magenta] r) Remove packages")
        console.print("\t[bold magenta] i) Install packages")
        console.print("\t[bold magenta] u) Update packages")
        console.print("\t[bold red] q) Quit")
        console.print("[bold italic white]> Choice:", end=" ")

    if(operation == 'r'):
        remove(isInteractive, packages=[], context=currentContext, console=console)
    elif(operation == 'i'):
        install(isInteractive, packages=[], context=currentContext, console=console)
    elif(operation == 'u'):
        update(isInteractive, packages=[], context=currentContext, console=console)
    elif(operation == 'q'):
        exit()
    else:
        console.print(':warning: An error has occurred.')
        exit()
