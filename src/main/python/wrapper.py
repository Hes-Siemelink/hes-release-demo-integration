# The below imports should always be the first in this file.
from __future__ import annotations
from release_sdk import BasePlugin
import logger_config
# The above imports should always be the first in this file.

import sys
import logging
import signal
from release_sdk import get_task_properties, create_output_context_file, AbortException, OutputContext
from example_api import ExampleApi
from example_abort import ExampleAbort

logger = logging.getLogger(__name__)

plugin: BasePlugin = BasePlugin()


def abort_handler(signum, frame):
    """ This method handles the abort request """
    logger.info("Received SIGTERM to gracefully stop the process")
    plugin.abort_job()


# Register abort handler
signal.signal(signal.SIGTERM, abort_handler)

if __name__ == "__main__":
    output_context: OutputContext = OutputContext(-1, {}, [])

    try:
        logger.debug("Preparing for task properties.")
        task_properties = get_task_properties()

        # Developer work area - start

        if task_properties['scriptLocation'] == 'example_api.py':
            plugin.task_object = ExampleApi(task_properties)
        elif task_properties['scriptLocation'] == 'example_abort.py':
            plugin.task_object = ExampleAbort(task_properties)

        # Developer work area - End

        logger.debug("Starting job execution.")
        output_context = plugin.execute_job()

    except AbortException:
        logger.debug("Abort requested")
        sys.exit(104)

    except Exception:
        logger.error("Unexpected error occurred.", exc_info=True)

    finally:
        logger.debug("Creating output context file")
        create_output_context_file(output_context)
