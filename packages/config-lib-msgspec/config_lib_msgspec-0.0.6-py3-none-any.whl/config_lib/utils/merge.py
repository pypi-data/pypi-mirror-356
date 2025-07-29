"""Module provides a function to recursively merge two configuration dictionaries.

It supports nested dictionaries, sequences, and scalar values.
Merging follows the rules:
    1. For scalar values (str, int, float, datetime.datetime, datetime.date, or None):
       if both target and source values are scalar, the source value takes precedence.
    2. For sequences (list or tuple):
       if both are sequences, the resulting sequence is the target sequence
       extended by any elements from the source sequence that are not already present.
    3. For mappings (dict):
       if both are mappings, the merge is performed recursively.
    4. If types (categories) differ for corresponding keys, a ValueError is raised.
    5. If a key exists in one dictionary but not the other or its value is None,
       the non-None value is used.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .types import is_mapping, is_scalar, is_sequence

if TYPE_CHECKING: # pragma: no cover
    from .types import ConfigMapping, ConfigScalar, ConfigSequence


def _merge_sequences(target_seq: ConfigSequence, source_seq: ConfigSequence) -> list[ConfigScalar]:
    """Merge two sequences according to union semantics while preserving order.

    Elements from source_seq that are already in target_seq will not be added again.

    Args:
        target_seq: The original sequence.
        source_seq: The sequence to merge.

    Returns:
        A new list representing the merged sequence.

    """
    return list(set(target_seq) | set(source_seq))


def _merge_values(left: Any, right: Any) -> Any:
    """Merge two configuration values according to their types.

    If one of the values is None, the other is returned.

    Args:
        left: The value from the target dictionary.
        right: The value from the source dictionary.

    Returns:
        The merged value.

    Raises:
        ValueError: When the types of left and right are incompatible for merging.

    """
    # Rule 5 and Rule 6: If either value is None, return the other.
    if right is None:
        return left
    if left is None:
        return right

    # If both are scalar values, source takes precedence.
    if is_scalar(left) and is_scalar(right):
        return right

    # If both are sequences, merge them.
    if is_sequence(left) and is_sequence(right):
        return _merge_sequences(left, right)

    # If both are mappings, merge them recursively.
    if is_mapping(left) and is_mapping(right):
        return update_recursive(left, right)

    # If types differ, raise ValueError.
    msg = f"Incompatible types for merging: {type(left).__name__} and {type(right).__name__}"
    raise ValueError(msg)


def update_recursive(target: ConfigMapping, source: ConfigMapping) -> ConfigMapping:
    """Recursively merge two configuration dictionaries according to predefined rules.

    For each key:
      - If the key exists in both dictionaries, the values are merged based on type.
      - If the key exists only in one dictionary, the non-None value is used.

    Args:
        target: The target configuration dictionary.
        source: The source configuration dictionary.

    Returns:
        A new configuration dictionary resulting from merging target and source.

    Raises:
        ValueError: If a value in target and source have incompatible types according to the rules.
        TypeError: If the provided arguments are not dictionaries.

    """
    if not (is_mapping(target) and is_mapping(source)):
        msg = "Both target and source must be dictionaries (mappings)."
        raise TypeError(msg)

    merged: ConfigMapping = {}

    # Get the union of keys from both dictionaries.
    all_keys = set(target.keys()) | set(source.keys())
    for key in all_keys:
        # Retrieve values, defaulting to None if the key does not exist.
        left_value = target.get(key, None)
        right_value = source.get(key, None)

        # If the key is in both dictionaries, merge the values.
        if key in target and key in source:
            merged[key] = _merge_values(left_value, right_value)
        elif key in target:
            # Rule 5: When source does not have a corresponding non-None value, use target.
            merged[key] = left_value
        else:
            # Rule 6: When target is missing or None, use the source value.
            merged[key] = right_value

    return merged
