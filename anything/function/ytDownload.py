import yt_dlp
import typer
import sys
import os

def proggres(stream, chunk, bytesRemaining):
    totalSize = stream.filesize
    bytesDownloaded = totalSize - bytesRemaining
    percentage = (bytesDownloaded / totalSize) * 100

    sys.stdout.write(f"Downloading... {percentage:.2f}%")
    sys.stdout.flush()

def ytDownload(url, type):
    try:
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        if type == "video":
            ydl_opts = {
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
            }

        else:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }]
            }

        typer.secho(f"Memulai download...", fg=typer.colors.YELLOW)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "Unknown Title")
            typer.secho(f"Judul: {title}\n", fg=typer.colors.CYAN, bold=True)

            ydl.download([url])

        typer.secho(f"\nDownload selesai", fg=typer.colors.GREEN, bold=True)

    except Exception as e:
        typer.secho(f"\n Terjadi kesalahan {e}", fg=typer.colors.RED)

