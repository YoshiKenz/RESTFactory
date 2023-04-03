# init logger_package
import logging.config

from core import config

config_path = "/".join([config.CONFIG_DIR, config.LOG_CONFIG_INI])

# timestamp = datetime.now().strftime("%d%m%Y-%H:%M:%S")
logging.config.fileConfig(
    config_path,
    disable_existing_loggers=False,
    # defaults={"logfilename": f"{LOG_DIR}/{timestamp}.log"},
)

logger = logging.getLogger()

logger.info("Welcome to RESTFactory")
