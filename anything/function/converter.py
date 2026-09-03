import tkinter as tk
from tkinter import filedialog
import typer
from pathlib import Path
from docx2pdf import convert
import os

def converter():
    root = tk.Tk()
    root.withdraw()

    selected_file = filedialog.askopenfilename(title="Select a file")
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")  

    if selected_file:
        file = Path(selected_file)
        extension = file.suffix.lower()

        if extension != ".docx":
            typer.secho(f"Ini bukan file word\n", fg=typer.colors.RED)
        else:
            typer.secho(f"File dipilih > {selected_file}\n", fg=typer.colors.GREEN)
            typer.secho(f"Memulai proses convert..\n", fg=typer.colors.BRIGHT_BLUE)

            output_file_name = file.stem + ".pdf"
            output_path = os.path.join(download_path, output_file_name)

            convert(selected_file, output_path)

            typer.secho(f"Berhasil disimpan di Downloads\n", fg=typer.colors.BRIGHT_BLUE)
    else:
        typer.secho(f"Proses dibatalkan\n", fg=typer.colors.RED)