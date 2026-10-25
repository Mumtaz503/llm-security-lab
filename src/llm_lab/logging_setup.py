import logging
import os


def config_logging() -> None:
    level = os.environ.get("LLM_LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
