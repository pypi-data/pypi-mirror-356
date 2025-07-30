"""Configuration management for Honor MCP."""

import json
import os
from pathlib import Path
from typing import Any

# Default configuration
DEFAULT_CONFIG = {"url_base": "http://localhost:7075", "user_agent": "honor-mcp/1.0"}


def get_config() -> dict[str, Any]:
    """Get configuration values from environment variables or config file.

    Priority order:
    1. Environment variables
    2. User config file (~/.config/honor-mcp/config.json)
    3. Default values
    """
    config = DEFAULT_CONFIG.copy()

    # Check for config file
    config_path = Path.home() / ".config" / "honor-mcp" / "config.json"
    if config_path.exists():
        try:
            with open(config_path) as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception:
            # If there's any error reading the config file, fall back to defaults
            pass

    # Environment variables override file config
    if "HONOR_MCP_URL_BASE" in os.environ:
        config["url_base"] = os.environ["HONOR_MCP_URL_BASE"]

    if "HONOR_MCP_USER_AGENT" in os.environ:
        config["user_agent"] = os.environ["HONOR_MCP_USER_AGENT"]

    # Ensure required environment variable is set
    if "HONOR_MCP_API_KEY" not in os.environ:
        raise ValueError("HONOR_MCP_API_KEY environment variable is required")
    config["honor_mcp_api_key"] = os.environ["HONOR_MCP_API_KEY"]

    return config
