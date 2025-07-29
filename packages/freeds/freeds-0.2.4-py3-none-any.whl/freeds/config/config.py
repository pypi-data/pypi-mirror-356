import logging
from typing import Any, cast

from freeds.config.api import get_config_from_api, is_api_avaiable, write_config_to_api
from freeds.config.file import get_config_from_file, write_config_to_file

logger = logging.getLogger(__name__)


def get_config(config_name: str) -> dict[str, Any]:
    """Get a config, from api server if available or from file if avaiable."""
    if not config_name:
        raise ValueError("A config_name must be provided.")

    if is_api_avaiable():
        logger.debug("Using API to get config: %s", config_name)
        cfg = get_config_from_api(config_name)
    else:
        logger.debug("Reading config from file: %s", config_name)
        cfg = get_config_from_file(config_name)
    # Tthose functions are typed correctly, but mypy still won't accept it.
    # Try to remove the cast when we're on newer python
    return cast(dict[str, Any], cfg)


def set_config(config_name: str, config: dict[str, Any]) -> None:
    if config is None:
        raise ValueError("Config cannot be None.")
    if config.get("config") is None:
        raise ValueError("Config must have config key.")
    if is_api_avaiable():
        write_config_to_api(config_name=config_name, config=config)
    else:
        write_config_to_file(config_name=config_name, config=config)
