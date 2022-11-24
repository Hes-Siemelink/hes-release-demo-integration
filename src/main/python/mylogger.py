import logging.config
import pkgutil
import yaml

config_file_data = pkgutil.get_data(__name__, "mylogger.yaml")

try:
    log_config = yaml.safe_load(config_file_data)
    logging.config.dictConfig(log_config)
except Exception as e:
    print(f'Error in Logging Configuration. Using default configs.\n{e}')
    logging.basicConfig(level=logging.INFO)
