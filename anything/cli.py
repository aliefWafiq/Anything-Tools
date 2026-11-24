from pathlib import Path
from typing import List
import typer
from anything import __app_name__, __version__
import pyfiglet
import shlex
from anything.function.ytDownload import ytDownload
from anything.function.converter import converter
from anything.function.framework import framework

from anything import ERRORS, __app_name__, __version__, config, database, rptodo

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="to-do database location?",
    ),
) -> None:
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        return
        
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED
        )
        return
    else:
        typer.secho(f"The to-do database is {db_path}",)

def get_todoer() -> rptodo.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
        if db_path is None:
            typer.secho(
                'Config file is invalid. Please run "anything init" again.',
                fg=typer.colors.RED,
            )
            return None
    else:
        typer.secho(    
            'Config file not found. Please run "anything init" first.',
            fg=typer.colors.RED,
        )
        return None
    
    if db_path.exists():
        return rptodo.Todoer(db_path)
    else:
        typer.secho(
            'Database not found. Please run "anything init" first.',
            fg=typer.colors.RED,
        )
        return None

@app.command()
def add(
    description: List[str] = typer.Argument(...),
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
) -> None:
    todoer = get_todoer()
    if todoer is None:
            return

    todo, error = todoer.add(description, priority)
    if error:
        typer.secho(
            f'Adding to-do failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
    else:
        typer.secho(
            f""" to-do: "{todo['Description']}" was added """
            f""" with priority: {priority} """,
            fg=typer.colors.GREEN,
        )

@app.command(name="todolist")
def todo_menu() -> None:
    while True:
        todoer = get_todoer()
        if todoer is None:
            break

        todo_list = todoer.get_todo_list()
        banner = pyfiglet.figlet_format("Anything", font="larry3d")
        typer.secho(banner, fg=typer.colors.BRIGHT_BLUE)

        if len(todo_list) == 0:
            typer.secho(
                "There are no tasks in your to-do list yet", fg=typer.colors.YELLOW
            )
        typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
        columns = (
            "ID. ",
            "| Priority ",
            "| Done ",
            "| Description ",
        )
        headers = "".join(columns)
        typer.secho(headers, fg=typer.colors.BLUE, bold=True)
        typer.secho("-" * len(headers), fg=typer.colors.BLUE)
        for id, todo in enumerate(todo_list, 1):
            desc = todo['Description'] 
            priority = todo['Priority']
            done = todo['Done']
            typer.secho(
                f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
                f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
                f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
                f"| {desc}",
            )
        typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)

        typer.secho(
            "- add <description> --priority <1-3>\n"
            "- complete <TODO_ID>\n" \
            "- remove <TODO_ID>\n"
            "- clear\n"
            "- back\n"
        )
        option = input("Anything (Todo) > ")

        if option.strip().lower() == "back":
            break

        try:
            args = shlex.split(option)
            app(args, standalone_mode=False)
        except Exception as e:
            typer.clear()
            typer.secho(f"Error: {e}", fg=typer.colors.RED)

@app.command(name="complete")
def set_done(todo_id: int = typer.Argument(...)) -> None:
    todoer = get_todoer()
    if todoer is None:
            return
    
    todo, error = todoer.set_done(todo_id)
    if error:
        typer.secho(ERRORS[error], fg=typer.colors.RED)
    else:
        typer.secho(
            f""" to-do #{todo_id} "{todo['Description']}" completed! """,
            fg=typer.colors.GREEN
        )


@app.command(name="remove")
def remove(
    todo_id: int = typer.Argument(...),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force deletion without confirmation",
    ),
) -> None:
    todoer = get_todoer()
    if todoer is None:
            return
    
    def _remove():
        todo, error = todoer.remove(todo_id)
        if error:
            typer.secho(
                f'Removing to-do # {todo_id} failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
        else:
            typer.secho(
                f"""to-do #{todo_id: } '{todo["Description"]}' was removed""",
                fg=typer.colors.GREEN,
            )
    
    if force:
        _remove()
    else:
        todo_list = todoer.get_todo_list()
        try:
            todo = todo_list[todo_id - 1]
        except IndexError:
            typer.secho("Invalid TODO_ID", fg=typer.colors.RED)
            return
        delete = typer.confirm(
            f"Delete to-do # {todo_id}: {todo['Description']}?"
        )
        if delete:
            _remove()
        else:
            typer.secho("Operation canceled")

@app.command(name="clear")
def remove_all(
    force: bool = typer.Option(
        ...,
        prompt="Delete all to-dos?",
        help="Force deletion without confirmation"
    ),
) -> None:
    todoer = get_todoer()
    if todoer is None:
        return

    if force:
        error = todoer.remove_all().error
        if error:
            typer.secho(
                f'Removing all to-dos failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
        else:
            typer.secho("All to-dos were removed", fg=typer.colors.GREEN)
    else:
        typer.secho("Operation canceled")

@app.command(name="ytDownloader")
def yt_downloader() -> None:
    banner = pyfiglet.figlet_format("Anything", font="larry3d")
    typer.secho(banner, fg=typer.colors.BRIGHT_BLUE)

    link = typer.prompt("Enter the video link ")

    typer.secho(
        "(1) Video\n"
        "(2) Audio\n"
        "(3) Back"
    )
    while True:
        option = input("Anything (Yt Downloader) > ").strip()

        if option.strip().lower() == "3":
            break

        else:
            ytDownload(link, option)

@app.command(name="wordToPDF")
def wordToPDF() -> None:
    banner = pyfiglet.figlet_format("Anything")
    typer.secho(banner, fg=typer.colors.BRIGHT_BLUE)
    converter()

@app.command(name="run")
def run() -> None:
    banner = pyfiglet.figlet_format("Anything", font="larry3d")
    typer.secho(banner, fg=typer.colors.BRIGHT_BLUE)
    framework()

@app.command(name="menu")
def menu() -> None:
    while True:
        typer.clear()

        banner = pyfiglet.figlet_format("Anything", font="larry3d")
        typer.secho(banner, fg=typer.colors.BRIGHT_BLUE)
        typer.secho(
            "list menu:\n\n"
            "(1) To do list\n"
            "(2) Yt downloader\n"
            "(3) Word to PDF\n"
            "(4) Build framework\n"
            "(5) exit\n"
        )
        option = input("Anything > ").strip()
    
        if option == "5":
            typer.secho("Bye!", fg=typer.colors.BRIGHT_BLUE)
            break

        elif option == "1":
            try:
                typer.clear()
                app(["todolist"], standalone_mode=False)
            except Exception as e:
                input("\nPress enter to go back to menu...")
                typer.secho(f"Back to menu...", fg=typer.colors.YELLOW)

        elif option == "2":
            try:
                typer.clear()
                app(["ytDownloader"], standalone_mode=False)
                input("\nPress enter to go back to menu...")
            except Exception as e:
                typer.secho(f"Back to menu...", fg=typer.colors.YELLOW)

        elif option == "3":
            try:
                typer.clear()
                app(["wordToPDF"], standalone_mode=False)
                input("\nPress enter to go back to menu...")
            except Exception as e:
                typer.secho(f"Back to menu...", fg=typer.colors.YELLOW)

        elif option == "4":
            try:
                typer.clear()
                app(["run"], standalone_mode=False)
                input("\nPress enter to go back to menu...")
            except Exception as e:
                typer.secho(f"Back to menu... {e}", fg=typer.colors.YELLOW)

        else:
            try:
                args = shlex.split(option)
                app(args, standalone_mode=False)
            except Exception as e:
                typer.secho(f"Error: {e}", fg=typer.colors.RED)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=_version_callback)
    ):
    if ctx.invoked_subcommand is None:
        menu()