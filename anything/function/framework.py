import typer
import subprocess
import tkinter as tk
from tkinter import filedialog

def framework():
    try:
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
            typer.secho(
                "\nSpecify the version you want or just enter to use the latest",
                fg=typer.colors.GREEN
            )
            framework_version = input("Enter framework version: ").strip()

            makeLaravel(framework_version, project_name, project_directory)

        elif framework.lower() == "next js":
            project_name = input("\nEnter the project name: ").strip()
            typer.secho(
                "\nSpecify the version you want or just enter to use the latest",
                fg=typer.colors.GREEN
            )
            framework_version = input("Enter framework version: ").strip()

            makeNextJs(framework_version, project_name, project_directory)

        else:
            typer.secho("Invalid framework. Please try again.", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"\n Terjadi kesalahan {e}", fg=typer.colors.RED)
            
def makeLaravel(version, project_name, project_directory):
    version_text = "the latest version" if version == "" else f"{version} version"
    subprocess.run(["composer", "create-project", "--prefer-dist", f"Laravel/laravel={version}", f"{project_directory}/{project_name}"], shell=True)
    if subprocess.CalledProcessError:
        typer.secho(
            f"No such version, please check if the version exist",
            fg=typer.colors.RED
        )
    else:
        typer.secho(
            f"Created Laravel project '{project_name}' with {version_text} on {project_directory}",
            fg=typer.colors.GREEN
        )

def makeNextJs(version, project_name, project_directory):
    version_text = "the latest version" if version == "" else f"{version} version"
    subprocess.run(["npx", f"create-next-app@{version}", f"{project_directory}/{project_name}"], shell=True)
    if subprocess.CalledProcessError:
        typer.secho(
            f"No such version, please check if the version exist",
            fg=typer.colors.RED
        )
    else:
        typer.secho(
            f"Created Next.js project '{project_name}' with {version_text} on {project_directory}...",
            fg=typer.colors.GREEN
        )