"""Module for converting flat dictionaries with delimited keys into nested dictionaries.

This module provides functions to process keys that use a specified delimiter to indicate
nested structure and to build nested dictionaries accordingly.
"""

from __future__ import annotations

from typing import Any

NEST_DELIMITER: str = "__"


def _split_key(key: str, delimiter: str = NEST_DELIMITER) -> list[str]:
    """Split the key using the given delimiter.

    Args:
        key: The key to split.
        delimiter: The delimiter used to separate key parts.

    Returns:
        A list of key parts, empty parts are preserved except for trailing ones.

    Raises:
        ValueError: If the key is exactly the delimiter.

    """
    if not key.replace(delimiter, ""):
        msg = f"Key cannot be only the delimiter: '{delimiter}'"
        raise ValueError(msg)

    # Special case: if key starts with delimiter, keep it as is
    if key.startswith(delimiter):
        return [key]

    # Split the key but preserve empty parts in the middle
    parts = key.split(delimiter)

    # Remove trailing empty parts only
    while parts and not parts[-1]:
        _ = parts.pop()

    return parts


def _insert_nested(
    current: dict[str, Any],
    parts: list[str],
    value: Any,
    full_key: str,
    delimiter: str = NEST_DELIMITER,
) -> None:
    """Insert the value into the nested dictionary according to the key parts.

    Args:
        current: The current level of the nested dictionary.
        parts: List of key parts representing the nesting path.
        value: The value to insert.
        full_key: The full original key, used for generating informative error messages.
        delimiter: The delimiter used to join parts for error reporting.

    Raises:
        ValueError: If a conflict occurs between nested and non-nested keys.

    """
    # Handle empty parts by joining them with the previous non-empty part
    processed_parts: list[str] = []
    current_part = parts[0]

    for part in parts[1:-1]:
        if part:
            # If we have accumulated parts, add them and start new
            if current_part:
                processed_parts.append(current_part)
            current_part = part
        else:
            # Add delimiter to the current part
            current_part += delimiter

    # Add the last accumulated part
    if current_part:
        processed_parts.append(current_part)

    # Add the final part
    processed_parts.append(parts[-1])

    # Now process the consolidated parts
    for i, part in enumerate(processed_parts[:-1]):
        if part in current:
            if not isinstance(current[part], dict):
                conflict_key = delimiter.join(processed_parts[: i + 1])
                msg = f"Conflicting keys: '{conflict_key}' conflicts with a non-nested key."
                raise ValueError(msg)
        else:
            current[part] = {}
        current = current[part]

    last_part = processed_parts[-1]
    if last_part in current and isinstance(current[last_part], dict):
        msg = f"Conflicting keys: '{full_key}' conflicts with existing nested dictionary."
        raise ValueError(msg)
    current[last_part] = value


def nest_dict(flat_dict: dict[str, str], delimiter: str = NEST_DELIMITER) -> dict[str, Any]:
    """Convert a flat dictionary with delimited keys to a nested dictionary.

    For example, {"a__b__c": 1, "a__d": 2} becomes {"a": {"b": {"c": 1}, "d": 2}}.

    Args:
        flat_dict: The flat dictionary to convert.
        delimiter: The delimiter used to separate nested keys.

    Returns:
        A nested dictionary mapping.

    Raises:
        ValueError: If a key contains only the delimiter or if there are conflicts
                    between nested and non-nested keys.

    """
    result: dict[str, Any] = {}

    # Process each key-value pair in the flat dictionary.

    for key, value in flat_dict.items():
        if not key:
            continue  # Skip empty keys

        parts = _split_key(key, delimiter)

        # Handle non-nested keys where no splitting was necessary.
        if len(parts) == 1:
            # If the key is the original key (like "__s"), keep it as is
            if key.startswith(delimiter) or delimiter not in key:
                # Check for conflicts with nested keys
                base_key = parts[0]
                if base_key in result:
                    # Check if the existing value is a dictionary
                    if isinstance(result[base_key], dict):
                        msg = f"Conflicting keys: '{key}' attempts to overwrite nested dictionary with scalar value."
                        raise ValueError(msg)
                else:
                    result[base_key] = value
            else:
                # Normal flat key processing
                result[key] = value
        else:
            _insert_nested(result, parts, value, key, delimiter)

    return result
