"""Module for retrieving and processing environment variables as configuration settings.

This module provides functionality to extract environment variables that start with a specified prefix,
strip the prefix, convert them to lowercase, and nest them into a hierarchical dictionary structure.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from config_lib.utils.nest import nest_dict

if TYPE_CHECKING:
    from config_lib.utils.types import ConfigMapping


def _prepare(key: str, prefix: str) -> str:
    prefix_len = len(prefix)
    return key[prefix_len:].lower()


def _get_prefixed_values(prefix: str) -> dict[str, str]:
    return {_prepare(key, prefix): value for key, value in os.environ.items() if key.startswith(prefix)}


def get_env_values(env_prefix: str) -> ConfigMapping:
    """Retrieve environment variables with a given prefix and nests them into a hierarchical dictionary.

    Environment variables starting with the specified prefix are extracted, the prefix is removed,
    keys are converted to lowercase, and then nested according to the presence of delimiters
    (e.g., '__') in the keys.

    Args:
        env_prefix: The prefix to filter environment variables.

    Returns:
        A ConfigMapping representing the nested dictionary structure of the environment variables.

    """
    flat_env_dict = _get_prefixed_values(env_prefix)
    return nest_dict(flat_env_dict)
