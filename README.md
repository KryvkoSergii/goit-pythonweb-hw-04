# Application for coping and sorting these files by extention.

## Features

The application recursively scans the <source> folder to locate files, identifies each file's extension, creates a folder named after the extension within the <destination> folder, and copies all files with the same extension into their corresponding folders.

## Installation

To install the required dependencies, run:

```sh
poetry install
```

## Configuration

Before running the application, ensure you have configured the necessary settings in the `config.py` file.

## Usage

To run the application, use the following command:

```sh
poetry run python .\sorter\main.py read_folder=<source> copy_file=<destination> --log_level=DEBUG
```

Replace `<source>` with the path to the folder containing the files you want to sort, and `<destination>` with the path to the folder where you want the sorted files to be copied.

## Command Line Options

- `read_folder`: The source folder containing files to be sorted.
- `copy_file`: The destination folder where sorted files will be copied.
- `--log_level`: The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).

## Examples

To sort files from `C:\source` to `D:\destination` with debug logging:

```sh
poetry run python .\sorter\main.py read_folder=C:\source copy_file=D:\destination --log_level=DEBUG
```

To get help on the application usage:

```sh
poetry run python .\sorter\main.py --help
```
