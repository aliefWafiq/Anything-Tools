import typer
import subprocess
import tkinter as tk
from tkinter import filedialog

def framework():
    try:
        root = tk.Tk()
        root.withdraw()
        status = True

        project_directory = filedialog.askdirectory(title="Select a directory for your project")

        while status:
            typer.secho(f"\nSelected project directory: {project_directory}", fg=typer.colors.GREEN)
            typer.secho(
                "\nSelect the framework :\n\n"
                "(1) Laravel\n"
                "(2) Next Js\n"
            )

            framework = input("Anything (framework)(1/2) > ").strip()

            if framework.lower() == "1":
                project_name = input("\nEnter the project name: ").strip()
                typer.secho(
                    "\nSpecify the version you want or just enter to use the latest",
                    fg=typer.colors.GREEN
                )
                framework_version = input("Enter framework version: ").strip()
                create = makeLaravel(framework_version, project_name, project_directory)

                if create == "Success":
                    status = False

            elif framework.lower() == "2":
                project_name = input("\nEnter the project name: ").strip()
                typer.secho(
                    "\nSpecify the version you want or just enter to use the latest",
                    fg=typer.colors.GREEN
                )
                framework_version = input("Enter framework version: ").strip()
                create = makeNextJs(framework_version, project_name, project_directory)

                if create == "Success":
                    status = False

            else:
                typer.secho("Invalid framework. Please try again.", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"\n Terjadi kesalahan {e}", fg=typer.colors.RED)
            
def makeLaravel(version, project_name, project_directory):
    version_text = "the latest version" if version == "" else f"{version} version"
    try:
        subprocess.check_output(["composer", "create-project", "--prefer-dist", f"Laravel/laravel={version}", f"{project_directory}/{project_name}"], shell=True)
        typer.secho(
            f"Created Laravel project '{project_name}' with {version_text} on {project_directory}",
            fg=typer.colors.GREEN
        )

        return "Success"
    except subprocess.CalledProcessError:
        typer.secho(
            f"Something went wrong, please check if the version exist",
            fg=typer.colors.RED
        )
        return "Failed"

def makeNextJs(version, project_name, project_directory):
    version_text = "the latest version" if version == "" else f"{version} version"
    try:
        subprocess.run(["npx", f"create-next-app@{version}", f"{project_directory}/{project_name}"], shell=True)
        typer.secho(
            f"Created Next.js project '{project_name}' with {version_text} on {project_directory}...",
            fg=typer.colors.GREEN
        )
        return "Success"
    except subprocess.CalledProcessError:
        typer.secho(
            f"Something went wrong, please check if the version exist",
            fg=typer.colors.RED
        )
        return "Failed"