# see https://peps.python.org/pep-0563/
from __future__ import annotations
import mylogger
import sys
import logging
import signal
from release_sdk import BasePlugin, AbortException
from example_api import ExampleApi
from example_abort import ExampleAbort

logger = logging.getLogger(__name__)

plugin: BasePlugin = BasePlugin()


def abort_handler(signum, frame):
    logger.info("Received SIGTERM to gracefully stop the process")
    plugin.abort_job()


signal.signal(signal.SIGTERM, abort_handler)

if __name__ == "__main__":
    try:
        logger.debug("Preparing for job execution")
        task_properties = plugin.get_task_properties()

        # Developer code area - start

        if task_properties['scriptLocation'] == 'product.py':
            plugin.task_object = ExampleApi(task_properties)
        elif task_properties['scriptLocation'] == 'example_abort.py':
            plugin.task_object = ExampleAbort(task_properties)

        # Developer code area - End

        plugin.execute_job()

    except AbortException as e:
        logger.debug("Abort requested")
        sys.exit(104)
    except Exception as e:
        logger.error("Unexpected error occurred.", exc_info=True)
    finally:
        logger.debug("Creating output context file")
        plugin.create_output_context_file()