import json
import os
from pathlib import Path
from typing import Any

import jsonschema
from dotenv import load_dotenv

load_dotenv()  # loads .env into os.environ


class ConfigError(Exception):
    """Raised when configuration is invalid."""

    pass


def get_config_path() -> Path:
    """Get the configuration file path."""
    # Check for user config first
    user_config = Path.home() / ".idea-cli" / "config.json"
    if user_config.exists():
        return user_config

    # Fall back to project default
    return Path(__file__).parent.parent / "config" / "default.json"


def load_schema() -> dict[str, Any]:
    """Load the JSON schema for configuration validation."""
    schema_path = Path(__file__).parent.parent / "config" / "schema.json"
    with open(schema_path) as f:
        return json.load(f)


def validate_config(config: dict[str, Any]) -> None:
    """Validate configuration against schema."""
    schema = load_schema()
    try:
        jsonschema.validate(config, schema)
    except jsonschema.ValidationError as e:
        raise ConfigError(f"Invalid configuration: {e.message}") from e


def load_config() -> dict[str, Any]:
    """Load and validate configuration from config file."""
    config_path = get_config_path()

    if not config_path.exists():
        raise ConfigError(
            f"Configuration file not found at {config_path}. "
            "Run 'idea init-config' to create one."
        )

    with open(config_path) as f:
        config = json.load(f)

    validate_config(config)
    return config


def is_demo_mode() -> bool:
    """Check if demo mode is enabled."""
    try:
        config = load_config()
        return config.get("demoMode", False)
    except ConfigError:
        # If config is missing/invalid, default to demo mode
        return True


def check_api_key(config: dict[str, Any], service: str) -> str:
    """Check if required API key is available."""
    if service == "validator":
        api_key_env = config["validator"]["apiKeyEnv"]
    elif service == "llm":
        api_key_env = config["models"]["apiKeyEnv"]
    elif service == "backend":
        api_key_env = config["backend"]["apiKeyEnv"]
    else:
        raise ValueError(f"Unknown service: {service}")

    # Check if demo mode is enabled in the config
    demo_mode = config.get("demoMode", False)

    # Skip placeholder values
    if api_key_env.startswith("<<<"):
        if demo_mode:
            return "demo-key"
        raise ConfigError(
            f"API key environment variable not configured. "
            f"Please set a real environment variable name for {service}.apiKeyEnv"
        )

    api_key = os.getenv(api_key_env)
    if not api_key:
        if demo_mode:
            return "demo-key"
        raise ConfigError(
            f"❌ Missing API key. Please set ${api_key_env} or enable demoMode in config."
        )

    return api_key


def get_env_var(name: str) -> str:
    """Get environment variable or raise error if not found."""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable {name} not set")
    return value


def init_user_config() -> Path:
    """Initialize user configuration file from default template."""
    user_config_dir = Path.home() / ".idea-cli"
    user_config_dir.mkdir(exist_ok=True)

    user_config_path = user_config_dir / "config.json"
    default_config_path = Path(__file__).parent.parent / "config" / "default.json"

    # Copy default config to user location
    with open(default_config_path) as f:
        config = json.load(f)

    with open(user_config_path, "w") as f:
        json.dump(config, f, indent=2)

    return user_config_path
