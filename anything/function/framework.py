import typer
import subprocess
import tkinter as tk
from tkinter import filedialog

def framework():
    root = tk.Tk()
    root.withdraw()

    project_directory = filedialog.askdirectory(title="Select a directory for your project")
    
    typer.secho(f"\nSelected project directory: {project_directory}", fg=typer.colors.GREEN)
    typer.secho(
        "\nSelect the framework :\n\n"
        "-Laravel\n"
        "-Next Js\n"
    )

    framework = input("Anything (framework) > ").strip()

    if framework.lower() == "laravel":
        project_name = input("\nEnter the project name: ").strip()
        framework_version = input("Enter framework version: ").strip()

        makeLaravel(framework_version, project_name, project_directory)

    elif framework.lower() == "next js":
        project_name = input("\nEnter the project name: ").strip()
        framework_version = input("Enter framework version: ").strip()

        makeNextJs(framework_version, project_name, project_directory)

    else:
        typer.secho("Invalid framework. Please try again.", fg=typer.colors.RED)
            
def makeLaravel(version, project_name, project_directory):
    subprocess.run(["composer", "create-project", "--prefer-dist", f"Laravel/laravel={version}", f"{project_directory}/{project_name}"], shell=True)
    print(f"Created Laravel project '{project_name}' with version {version} on {project_directory}")

def makeNextJs(version, project_name, project_directory):
    subprocess.run(["npx", f"create-next-app@{version}", f"{project_directory}/{project_name}"], shell=True)
    print(f"Created Next.js project '{project_name}' with version {version} on {project_directory}...")