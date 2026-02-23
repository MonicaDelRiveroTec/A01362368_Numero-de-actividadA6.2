"""Shared file persistence utilities for all models."""

import json
import os


def load_data(filepath):
    """Load a JSON file and return its contents as a dict.

    Returns an empty dict if the file does not exist or contains invalid data.
    Errors are printed to the console and execution continues.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError) as error:
        print(f"[ERROR] Failed to load data from '{filepath}': {error}")
        return {}


def save_data(filepath, data):
    """Persist a dict to a JSON file.

    Errors are printed to the console and execution continues.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    except IOError as error:
        print(f"[ERROR] Failed to save data to '{filepath}': {error}")
