import json


def read_file(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)

    except FileNotFoundError:
        input(f"File {filename} not found. Press enter to close.")
        exit()
