import os

from src.configuration import (
    get_available_providers,
    get_provider_environment_variables,
)
from src.shared.log import logger


def verify_env_vars_are_correctly_setup() -> bool:
    env_vars_are_setup = True

    if len(get_available_providers()) == 0:
        logger.warning(
            f"No provider configured. To configure a provider, set the following env variables:\n{get_provider_environment_variables()}"
        )
        env_vars_are_setup = False
    if os.getenv("BACKEND_URL") is None:
        logger.warning(
            "BACKEND_URL is not set. Please set it the to point to your Core AI Service."
        )
        env_vars_are_setup = False

    return env_vars_are_setup
