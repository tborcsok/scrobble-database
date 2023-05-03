# scrobble-database

This is a CLI application that keeps a local record of your Last.fm library and listening history. The data is stored in an SQLite file and can be utilized for various reports and analyses.

## Prerequisites

To use the application, you need to have a Last.fm API key. To get an API key, apply [here](https://www.last.fm/api/account/create).

The application reads this info from a text file in this folder named `.env`. The `.env.example` file serves as a template for the `.env` file.

## Installation and usage

To run the application, prepare a Python environment with the dependencies defined in `pyproject.toml`. The tool for environment management used in this repository is Poetry. To prepare the environment run `poetry install`.

To run the CLI, activate the environment with e.g. the `poetry shell` command, then run the application with `python main.py --help` to see the available commands.

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  artist    Collect data about artists
  db        Database maintenance functions
  pipeline  Data collection pipeline that collects all data types
  track     Collect data about tracks
```

## Data overview

Tables:

| Table    | Description                                                                                     |
| -------- | ----------------------------------------------------------------------------------------------- |
| scrobble | Tracks listened to with timestamp and artist, album and track IDs                               |
| tag      | Collection of tags attached to artists (e.g. genre, country), provided by the Last.fm community |
| similar  | Collection of artists similar to each other, provided by the Last.fm community                  |
