import yt_dlp
import typer
import os

def ytDownload(url, type):
    try:
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        if type.lower() == "1":
            ydl_opts = {
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
            }
        elif type.lower() == "2":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }]
            }
        else:
            typer.secho(f"\n Invalid option", fg=typer.colors.RED)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                typer.secho(f"Starting download...", fg=typer.colors.YELLOW)
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "Unknown Title")
                typer.secho(f"Title: {title}\n", fg=typer.colors.CYAN, bold=True)

                ydl.download([url])

            typer.secho(f"\nDownload finished", fg=typer.colors.GREEN, bold=True)
            
        except Exception as e:
            typer.secho(f"Please try again", fg=typer.colors.RED)

    except Exception as e:
        typer.secho(f"\n Error {e}", fg=typer.colors.RED)

