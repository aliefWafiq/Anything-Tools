# ANYTHING Tools

A versatile Command Line Interface (CLI) application built with Python. It bundles several handy utilities into a single, easy-to-use tool to help streamline your daily tasks.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Troubleshooting](#troubleshooting)
- [Development Status](#development-status)

## Features

| Tool | Description |
|------|-------------|
| **Todo List** | Add, view, complete, and remove tasks right from the terminal. Tasks have priorities (1-3). |
| **YouTube Downloader** | Download videos (MP4) or audio (MP3) from YouTube using `yt-dlp`. |
| **Word to PDF Converter** | Convert `.docx` documents to PDF through a file picker. |
| **Project Scaffolder** | Create a new Laravel or Next.js project, with an optional version, in a folder you choose. |

## Prerequisites

### Required for everything

| Requirement | Version | Notes |
|-------------|---------|-------|
| [Python](https://www.python.org/downloads/) | 3.9 or newer | Tick **"Add Python to PATH"** during installation on Windows. |
| pip | Included with Python | Used to install the dependencies. |
| Git | Any recent version | Only needed to clone the repository. |

> **Tkinter** (used for file/folder dialogs) ships with Python on Windows and macOS. On Debian/Ubuntu, install it with `sudo apt install python3-tk`.

### Required per feature

You only need the items for the tools you plan to use.

| Feature | Extra requirement | Why |
|---------|-------------------|-----|
| Todo List | None | Works out of the box. |
| YouTube Downloader | [FFmpeg](https://ffmpeg.org/download.html) in your `PATH` | Converts audio to MP3 and merges video and audio streams. |
| Word to PDF | **Microsoft Word** installed | `docx2pdf` uses Word to do the conversion (Windows or macOS). |
| Scaffold: Laravel | [PHP](https://www.php.net/downloads) and [Composer](https://getcomposer.org/download/) | Runs `composer create-project`. |
| Scaffold: Next.js | [Node.js](https://nodejs.org/) (includes `npm` and `npx`) | Runs `npx create-next-app`. |

Check that everything is available:

```bash
python --version      # or: py --version
ffmpeg -version
composer --version
node --version
```

### Python dependencies

Installed automatically in the next step (see `requirements.txt`):

- [`typer`](https://typer.tiangolo.com/): CLI framework
- `colorama`, `shellingham`: terminal colors and shell detection
- `pyfiglet`: ASCII banner
- `yt-dlp`: YouTube downloading
- `docx2pdf`: Word to PDF conversion
- `pytest`: running the test suite

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/aliefWafiq/Anything-Tools.git
   cd Anything-Tools
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   # Windows
   py -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Getting Started

You only need two commands to start.

**1. Initialize the configuration** (run this first)

```bash
py -m anything init
```

You will be asked where the to-do database file should be stored. Press Enter to accept the default (a hidden JSON file in your home folder).

**2. Open the main menu**

```bash
py -m anything menu
```

```text
(1) To do list
(2) Yt downloader
(3) Word to PDF
(4) Build framework
(5) exit
```

> On macOS/Linux, replace `py` with `python3`.

## Usage

Every tool can be opened from the menu, or called directly as a command.

### Todo List

```bash
py -m anything todolist                      # interactive to-do menu
py -m anything add "Buy groceries" -p 1      # add a task (priority 1 = high, 3 = low, default 2)
py -m anything complete 1                    # mark task #1 as done
py -m anything remove 1                      # remove task #1 (asks for confirmation)
py -m anything remove 1 --force              # remove without confirmation
py -m anything clear                         # remove all tasks (asks for confirmation)
```

### YouTube Downloader

```bash
py -m anything ytDownloader
```

Paste a video URL, then choose `video` or `audio`. Files are saved to your **Downloads** folder.

### Word to PDF

```bash
py -m anything wordToPDF
```

A file picker opens, select a `.docx` file, and the PDF is saved to your **Downloads** folder.

### Project Scaffolder

```bash
py -m anything run
```

Choose **Laravel** or **Next.js**, enter a project name and (optionally) a version, then pick the destination folder. Leave the version empty to use the latest release.

### Other

```bash
py -m anything --version
py -m anything --help
```

## Project Structure

```text
Anything-Tools/
├── anything/
│   ├── __init__.py          # app name, version, error codes
│   ├── __main__.py          # entry point (py -m anything)
│   ├── cli.py               # Typer commands and menus
│   ├── config.py            # config file handling
│   ├── database.py          # JSON database for the to-do list
│   ├── rptodo.py            # to-do business logic
│   └── function/
│       ├── converter.py     # Word to PDF
│       ├── framework.py     # Laravel / Next.js scaffolder
│       └── ytDownload.py    # YouTube downloader
├── tests/
│   └── test_rptodo.py
├── requirements.txt
└── README.md
```

## Running Tests

```bash
pytest          # run all tests
pytest -v       # verbose output
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `'py' is not recognized` | Use `python` instead, or reinstall Python with the launcher option enabled. |
| `Config file not found. Run "init" first.` | Run `py -m anything init` once before using the to-do list. |
| YouTube audio download fails | Make sure FFmpeg is installed and available in your `PATH`. |
| Word to PDF fails | Close the `.docx` file if it is open, and make sure Microsoft Word is installed. |
| `'composer' / 'npx' not found` | Install Composer (Laravel) or Node.js (Next.js) and restart your terminal. |
| Folder dialog does not appear on Linux | Install Tkinter: `sudo apt install python3-tk`. |

## Development Status

This project is under active development. Some features are still a work in progress and may change in the future. Issues and suggestions are welcome.