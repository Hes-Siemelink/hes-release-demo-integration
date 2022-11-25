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
    """ This method handles the abort request """
    logger.info("Received SIGTERM to gracefully stop the process")
    plugin.abort_job()


signal.signal(signal.SIGTERM, abort_handler)

if __name__ == "__main__":
    try:
        logger.debug("Preparing for task properties.")
        task_properties = plugin.get_task_properties()

        # Developer code area - start

        if task_properties['scriptLocation'] == 'example_api.py':
            plugin.task_object = ExampleApi(task_properties)
        elif task_properties['scriptLocation'] == 'example_abort.py':
            plugin.task_object = ExampleAbort(task_properties)

        # Developer code area - End

        logger.debug("Starting job execution.")
        plugin.execute_job()

    except AbortException:
        logger.debug("Abort requested")
        sys.exit(104)
    except Exception:
        logger.error("Unexpected error occurred.", exc_info=True)
    finally:
        logger.debug("Creating output context file")
        plugin.create_output_context_file()
