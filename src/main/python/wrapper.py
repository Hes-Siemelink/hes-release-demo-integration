# base_config import should always be the first in this file.
from dai_release_sdk import base_config

import logging
from dai_release_sdk import get_task_properties, setup_logging, execute_task
from example_api import ExampleApi
from example_abort import ExampleAbort

setup_logging(package=__name__, file_name="logger.yaml", default_level=logging.INFO)

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    task_properties = get_task_properties()
    task_object = None

    if task_properties:
        if task_properties['scriptLocation'] == 'example_api.py':
            task_object = ExampleApi(task_properties)
        elif task_properties['scriptLocation'] == 'example_abort.py':
            task_object = ExampleAbort(task_properties)

        # Executing the task
        execute_task(task_object)
