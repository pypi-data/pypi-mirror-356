import os
from pathlib import Path

import msgspec
import pytest

from config_lib.base import BaseConfig


class SampleConfig(BaseConfig):
    """Sample configuration class for testing."""

    param1: str = "default1"
    param2: int = 123


class NestedParam(msgspec.Struct):
    param1: str = "default"
    param2: int = 123


class NestedConfig(BaseConfig):
    """Nested configuration class for testing."""

    nested_param: NestedParam = msgspec.field(default_factory=NestedParam)


class ErrorConfig(BaseConfig):
    """Configuration class for testing error handling."""

    required_param: str
    optional_param: int = 42


def test_base_config_defaults() -> None:
    """Test that default values are loaded correctly."""
    config = SampleConfig.load()
    assert config.param1 == "default1"
    assert config.param2 == 123


def test_base_config_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test loading configuration from environment variables."""
    monkeypatch.setenv("CFG_PARAM1", "env_value1")
    monkeypatch.setenv("CFG_PARAM2", "456")
    config = SampleConfig.load()
    assert config.param1 == "env_value1"
    assert config.param2 == 456


def test_base_config_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test loading configuration from command-line arguments."""
    monkeypatch.setattr("sys.argv", ["script_name", "--param1", "cli_value1", "--param2", "789"])
    config = SampleConfig.load()
    assert config.param1 == "cli_value1"
    assert config.param2 == 789


def test_base_config_yaml(tmp_path: Path) -> None:
    """Test loading configuration from a YAML file."""
    config_file = tmp_path / "config.yaml"
    _ = config_file.write_text("param1: yaml_value1\nparam2: 999")
    os.environ["CFG_CONFIG"] = str(config_file)  # Simulate CLI config path
    config = SampleConfig.load()
    assert config.param1 == "yaml_value1"
    assert config.param2 == 999


def test_base_config_precedence(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test that CLI arguments take precedence over environment variables and YAML."""
    config_file = tmp_path / "config.yaml"
    _ = config_file.write_text("param1: yaml_value1\nparam2: 999")
    os.environ["CFG_CONFIG"] = str(config_file)
    monkeypatch.setenv("CFG_PARAM1", "env_value1")
    monkeypatch.setenv("CFG_PARAM2", "456")
    monkeypatch.setattr("sys.argv", ["script_name", "--param1", "cli_value1", "--param2", "789"])
    config = SampleConfig.load()
    assert config.param1 == "cli_value1"
    assert config.param2 == 789


def test_nested_config_defaults() -> None:
    """Test that default values are loaded correctly for nested configs."""
    config = NestedConfig.load()
    assert config.nested_param.param1 == "default"
    assert config.nested_param.param2 == 123


def test_nested_config_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test loading nested configuration from environment variables."""
    monkeypatch.setenv("CFG_NESTED_PARAM__PARAM1", "env_value1")
    monkeypatch.setenv("CFG_NESTED_PARAM__PARAM2", "456")
    config = NestedConfig.load()
    assert config.nested_param.param1 == "env_value1"
    assert config.nested_param.param2 == 456


def test_nested_config_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test loading nested configuration from command-line arguments."""
    monkeypatch.setattr(
        "sys.argv",
        ["script_name", "--nested_param.param1", "cli_value1", "--nested_param.param2", "789"],
    )
    config = NestedConfig.load()
    assert config.nested_param.param1 == "cli_value1"
    assert config.nested_param.param2 == 789


def test_nested_config_yaml(tmp_path: Path) -> None:
    """Test loading nested configuration from a YAML file."""
    config_file = tmp_path / "config.yaml"
    _ = config_file.write_text("nested_param:\n  param1: yaml_value1\n  param2: 999")
    os.environ["CFG_CONFIG"] = str(config_file)  # Simulate CLI config path
    config = NestedConfig.load()
    assert config.nested_param.param1 == "yaml_value1"
    assert config.nested_param.param2 == 999


def test_nested_config_precedence(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test that CLI arguments take precedence over environment variables and YAML for nested configs."""
    config_file = tmp_path / "config.yaml"
    _ = config_file.write_text("nested_param:\n  param1: yaml_value1\n  param2: 999")
    os.environ["CFG_CONFIG"] = str(config_file)
    monkeypatch.setenv("CFG_NESTED_PARAM__PARAM1", "env_value1")
    monkeypatch.setenv("CFG_NESTED_PARAM__PARAM2", "456")
    monkeypatch.setattr(
        "sys.argv",
        ["script_name", "--nested_param.param1", "cli_value1", "--nested_param.param2", "789"],
    )
    config = NestedConfig.load()
    assert config.nested_param.param1 == "cli_value1"
    assert config.nested_param.param2 == 789


def test_config_missing_required_param() -> None:
    """Test that loading fails when a required parameter is missing."""
    with pytest.raises(msgspec.ValidationError, match="missing required field"):
        _ = ErrorConfig.load()


def test_config_invalid_cli_type(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test handling of CLI argument type conversion errors."""
    monkeypatch.setattr("sys.argv", ["script_name", "--required_param", "test_value", "--optional_param", "not_an_int"])
    with pytest.raises(msgspec.ValidationError, match="missing required field"):
        _ = ErrorConfig.load()


def test_config_env_parse_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CFG_NESTED_PARAM__PARAM1", "env_value1")
    monkeypatch.setenv("CFG_NESTED_PARAM", "456")
    with pytest.raises(msgspec.ValidationError, match="missing required field"):
        _ = ErrorConfig.load()


def test_config_merge_sources_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CFG_NESTED_PARAM", "456")
    config_file = tmp_path / "config.yaml"
    _ = config_file.write_text("nested_param:\n  param1: yaml_value1\n  param2: 999")
    with pytest.raises(ValueError, match="Incompatible types for merging"):
        _ = NestedConfig.load()


def test_config_yaml_parse_error(tmp_path: Path) -> None:
    """Test handling of invalid YAML file."""
    # Create an invalid YAML file
    config_file = tmp_path / "invalid_config.yaml"
    _ = config_file.write_text(": invalid yaml syntax")

    # Set the config path via environment variable
    os.environ["CFG_CONFIG"] = str(config_file)

    # The load method should log a warning and continue with an empty config
    with pytest.raises(ValueError, match="An error occurred while parsing the YAML file"):
        _ = ErrorConfig.load()


def test_config_nonexistent_yaml_file(tmp_path: Path) -> None:
    """Test handling of a non-existent YAML file."""
    # Use a path to a non-existent file
    nonexistent_config = tmp_path / "nonexistent_config.yaml"

    # Set the config path via environment variable
    os.environ["CFG_CONFIG"] = str(nonexistent_config)

    # The load method should log a warning and continue with an empty config
    with pytest.raises(msgspec.ValidationError):
        _ = ErrorConfig.load()


def test_config_env_type_conversion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test handling of environment variable type conversion errors."""
    # Set a non-integer value for an integer parameter
    monkeypatch.setenv("CFG_OPTIONAL_PARAM", "not_an_int")
    monkeypatch.setenv("CFG_REQUIRED_PARAM", "test_value")

    with pytest.raises(msgspec.ValidationError, match="Expected `int`"):
        _ = ErrorConfig.load()


def test_config_multiple_source_conflicts(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test handling of conflicting configuration sources."""
    # Create a YAML file
    config_file = tmp_path / "config.yaml"
    _ = config_file.write_text("required_param: yaml_value\noptional_param: 100")

    # Set environment variables
    monkeypatch.setenv("CFG_REQUIRED_PARAM", "env_value")
    monkeypatch.setenv("CFG_OPTIONAL_PARAM", "200")
    monkeypatch.setenv("CFG_CONFIG", str(config_file))

    # Set CLI arguments
    monkeypatch.setattr("sys.argv", ["script_name", "--required_param", "cli_value", "--optional_param", "300"])

    # Load config and verify CLI takes precedence
    config = ErrorConfig.load()
    assert config.required_param == "cli_value"
    assert config.optional_param == 300
