# Config-Lib

A lightweight configuration management library for Python applications that supports multiple sources (YAML, environment variables, CLI arguments) with type validation and automatic merging.


## Features

- **Multiple Configuration Sources**  
  Load from YAML files, environment variables, and command-line arguments
- **Precedence Hierarchy**  
  CLI arguments > Environment variables > YAML config files > Default values
- **Type Annotations**  
  Built on `msgspec` for robust type validation and serialization
- **Nested Configurations**  
  Support for complex nested structures with dot/bracket notation
- **Error Handling**  
  Clear validation errors and graceful handling of source failures

## Installation

```bash
pip install config-lib
```

## Basic Usage

```python
from config_lib.base import BaseConfig

class AppConfig(BaseConfig):
    """Main application configuration"""
    host: str = "localhost"
    port: int = 8080
    debug: bool = False

config = AppConfig.load()
```

## Configuration Sources

### YAML File
```yaml
# config.yaml
host: "0.0.0.0"
port: 9000
```

```python
os.environ["CFG_CONFIG"] = "config.yaml"
config = AppConfig.load()  # Loads from YAML
```

### Environment Variables
```bash
export CFG_HOST="127.0.0.1"
export CFG_PORT=3000
```

### CLI Arguments
```bash
python app.py --host 192.168.1.1 --port 4000
```

## Nested Configurations

```python
from msgspec import Struct

class DatabaseConfig(Struct):
    host: str = "localhost"
    port: int = 5432

class AppConfig(BaseConfig):
    db: DatabaseConfig = DatabaseConfig()
    cache_ttl: int = 300
```

**Environment variables**:  
`CFG_DB__HOST=postgres.example.com CFG_DB__PORT=6432`

**CLI arguments**:  
`python app.py --db.host postgres.example.com --db.port 6432`

## Precedence Rules

1. **Command-line arguments** (highest priority)
2. **Environment variables**
3. **YAML configuration file** (lowest priority)
4. **Class defaults** (used if no other sources provide values)

## Error Handling & Validation

The library provides:
- Automatic type validation using `msgspec`
- Clear error messages for missing required fields
- Graceful handling of malformed configuration sources
- Warning logging for source loading errors

## Contributing

```bash
# Run tests
pytest tests/

# Check test coverage
pytest --cov=config_lib --cov-report=html
```

Contributions welcome! Please follow standard Python packaging practices and ensure all tests pass before submitting PRs.

## License

MIT License. See [LICENSE](LICENSE) for details.
