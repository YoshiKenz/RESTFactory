# init logger_package
import logging.config
import os

from core import config


config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config.LOG_CONFIG_INI)


# timestamp = datetime.now().strftime("%d%m%Y-%H:%M:%S")
logging.config.fileConfig(
    config_path,
    disable_existing_loggers=False,
    # defaults={"logfilename": f"{LOG_DIR}/{timestamp}.log"},
)

logger = logging.getLogger()

logger.info("Welcome to RESTFactory")
