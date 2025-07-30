from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.router import router
from src.shared.log import logger
from src.shared.setup_helper import verify_env_vars_are_correctly_setup
from src.shared.utils import get_version

load_dotenv()
app = FastAPI(title="Evaluation", version=get_version())
app.include_router(router)

if not verify_env_vars_are_correctly_setup():
    logger.error("Environment variables are not set up correctly.")
