import typer
import subprocess
import tkinter as tk
from tkinter import filedialog
import shutil
from pathlib import Path

def framework():
    try:
        root = tk.Tk()
        root.withdraw()
        status = True
        notSelected = True

        while notSelected:
            project_directory = filedialog.askdirectory(title="Select a directory for your project")

            if project_directory != "":
                notSelected = False

        while status:
            typer.secho(f"\nSelected project directory: {project_directory}", fg=typer.colors.GREEN)
            typer.secho(
                "\nSelect the framework :\n\n"
                "(1) Laravel\n"
                "(2) Next Js\n"
                "(3) Back"
            )

            framework = input("Anything (framework)(1/2/3) > ").strip()

            if framework == "1":
                project_name = input("\nEnter the project name: ").strip()
                typer.secho(
                    "\nSpecify the version you want or just enter to use the latest",
                    fg=typer.colors.GREEN
                )
                framework_version = input("Enter framework version: ").strip()
                create = makeLaravel(framework_version, project_name, project_directory)

                if create == "Success":
                    status = False

            elif framework == "2":
                project_name = input("\nEnter the project name: ").strip()
                typer.secho(
                    "\nSpecify the version you want or just enter to use the latest",
                    fg=typer.colors.GREEN
                )
                framework_version = input("Enter framework version: ").strip()
                create = makeNextJs(framework_version, project_name, project_directory)

                if create == "Success":
                    status = False
            elif framework == "3":
                break
            else:
                typer.secho("Invalid framework. Please try again.", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"\n Terjadi kesalahan {e}", fg=typer.colors.RED)
            
def _run(cmd: list[str]) -> bool:
    exe = shutil.which(cmd[0])
    if exe is None:
        typer.secho(f"'{cmd[0]}' not found, please check if its installed",
                    fg=typer.colors.RED)
        return False
    try:
        subprocess.run([exe, *cmd[1:]], check=True)
        return True
    except subprocess.CalledProcessError:
        typer.secho("Please check if the version exist", fg=typer.colors.RED)
        return False

def makeLaravel(version, project_name, project_directory):
    target = str(Path(project_directory) / project_name)
    package = f"laravel/laravel:{version}" if version else "laravel/laravel"
    ok = _run(["composer", "create-project", "--prefer-dist", package, target])
    return "Success" if ok else "Failed"

def makeNextJs(version, project_name, project_directory):
    target = str(Path(project_directory) / project_name)
    pkg = f"create-next-app@{version}" if version else "create-next-app@latest"
    ok = _run(["npx", pkg, target])
    return "Success" if ok else "Failed"