import tkinter as tk
from tkinter import filedialog
import typer
from pathlib import Path
from docx2pdf import convert
import os

def converter():
    try:
        root = tk.Tk()
        root.withdraw()

        selected_file = filedialog.askopenfilename(title="Select a file")
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")  

        if selected_file:
            file = Path(selected_file)
            extension = file.suffix.lower()

            if extension != ".docx":
                typer.secho(f"This file is not a word\n", fg=typer.colors.RED)
            else:
                typer.secho(f"Selected file > {selected_file}\n", fg=typer.colors.GREEN)
                typer.secho(f"Converting..\n", fg=typer.colors.BRIGHT_BLUE)

                output_file_name = file.stem + ".pdf"
                output_path = os.path.join(download_path, output_file_name)

                convert(selected_file, output_path)

                typer.secho(f"Successfully saved to Downloads\n", fg=typer.colors.BRIGHT_BLUE)
        else:
            typer.secho(f"Process canceled\n", fg=typer.colors.RED)
    except Exception as e:
        typer(f"Eror {e}", fg=typer.colors.RED)