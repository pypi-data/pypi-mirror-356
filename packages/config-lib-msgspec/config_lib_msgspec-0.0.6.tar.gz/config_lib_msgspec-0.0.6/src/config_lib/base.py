"""Base class for configuration with loading from multiple sources."""
from __future__ import annotations

import logging
from typing import ClassVar

import msgspec
from yaml import YAMLError

from config_lib.sources.cli import get_cli_values
from config_lib.sources.env import get_env_values
from config_lib.sources.yaml import get_yaml_values
from config_lib.utils.merge import update_recursive

SOURCES_MAP = {
    "cli": get_cli_values,
    "yaml": get_yaml_values,
    "env": get_env_values,
}

logger = logging.getLogger(__name__)


class ConfigSourceError(Exception):
    """Base class for configuration source errors."""



class ConfigParseError(Exception):
    """Base class for configuration parsing errors."""



class BaseConfig(msgspec.Struct):
    """Base class for configuration, providing loading from environment, YAML files, and CLI arguments.

    Configuration is loaded in the following order, with later sources overriding earlier ones:
    1. YAML file (if specified via CLI)
    2. Environment variables (prefixed with `env_prefix`)
    3. CLI arguments

    Attributes:
        env_prefix: The prefix for environment variables (default: "CFG_").

    """

    env_prefix: ClassVar[str] = "CFG_"

    @classmethod
    def load(cls) -> BaseConfig:
        """Load configuration from available sources.

        Returns:
            An instance of the configuration class with values loaded from YAML, environment, and CLI.

        """
        try:
            cli_values = get_cli_values(cls)
        except ValueError as err:
            logger.warning("unable to load cli values: %s", err)
            cli_values = {}

        try:
            env_values = get_env_values(env_prefix=cls.env_prefix)
        except ValueError as err:
            logger.warning("unable to load env values: %s", err)
            env_values = {}

        config_path: str | None = cli_values.get("config", None) or env_values.get("config", None)  # pyright: ignore[reportUnknownMemberType, reportAssignmentType]
        try:
            yaml_values = get_yaml_values(config_path)
        except (FileNotFoundError, YAMLError) as err:
            logger.warning("unable to load config from %s values: %s", config_path, err)
            yaml_values = {}

        merged_data = update_recursive(yaml_values, update_recursive(env_values, cli_values))  # pyright: ignore[reportUnknownArgumentType]

        return msgspec.convert(merged_data, type=cls, strict=False)
