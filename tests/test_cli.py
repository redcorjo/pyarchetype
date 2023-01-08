import os
import logging
import pyarchetype

level = os.getenv("LOGGER", "INFO")
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

logger.info("Run tests")