from logging import Logger, config as logger_config
import json
import os


def get_logger(logger_name: str = "Root") -> Logger:
    file_path: str = (os.path.dirname(__file__)) + '/logger_config.json'

    with open(file_path) as config_file:
        config = json.load(config_file)

    logger_config.dictConfig(config)
    return logger_config.logging.getLogger(logger_name)


logger: Logger = get_logger()
