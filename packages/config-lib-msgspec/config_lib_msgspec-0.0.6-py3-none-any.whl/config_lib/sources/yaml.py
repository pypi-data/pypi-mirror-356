"""Provides functionality to read and parse YAML files into a ConfigMapping."""

from __future__ import annotations

from pathlib import Path

import yaml

from config_lib.utils.types import ConfigMapping, is_mapping


def get_yaml_values(file_path: str | None) -> ConfigMapping:
    """Read and parse a YAML file into a ConfigMapping.

    Args:
        file_path: The path to the YAML file. If None, an empty ConfigMapping is returned.

    Returns:
        A ConfigMapping containing the parsed data from the YAML file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If the file cannot be read.
        yaml.YAMLError: If the file cannot be parsed as YAML.

    """
    if file_path is None:
        return {}

    path = Path(file_path)
    if not path.exists():
        msg = f"The file {file_path} does not exist."
        raise FileNotFoundError(msg)

    try:
        with path.open("r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
            if not is_mapping(yaml_data):
                msg = f"The parsed data is not a ConfigMapping, but {type(yaml_data).__name__}."
                raise ValueError(msg)
            return yaml_data
    except OSError as e: # pragma: no cover
        msg = f"An error occurred while reading the file {file_path}: {e}"
        raise ValueError(msg) from None
    except yaml.YAMLError as e:
        msg = f"An error occurred while parsing the YAML file {file_path}: {e}"
        raise ValueError(msg) from None
