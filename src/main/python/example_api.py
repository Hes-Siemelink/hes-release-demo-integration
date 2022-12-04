import logging
import sys

import requests
from requests import HTTPError

from dai_release_sdk import BaseTask, OutputContext, AbortException

logger = logging.getLogger(__name__)


class ExampleApi(BaseTask):
    """ The developer should extend the BaseTask and override the 'exec' and 'abort' methods."""

    def __init__(self, params):
        self.params = params
        self.task_id = params['task_id']
        self.title = None
        self.brand = None

    def exec(self) -> OutputContext:
        """ Here is the task logic. It should return 'OutputContext' object. """

        output_context: OutputContext = OutputContext(-1, {}, [])
        logger.debug(f"Task property values are  : {self.params}")

        try:
            request_url = self.params['url'] + self.params['productId']
            self.__add_comment__(f"Request URL is {request_url}")
            response = requests.get(request_url)
            response.raise_for_status()
            self.title = response.json()['title']
            self.brand = response.json()['brand']
            output_context.exit_code = 0

        except HTTPError:
            logger.error("Http Error error occurred.", exc_info=True)
            output_context.exit_code = 101

        except Exception:
            logger.error("Unexpected error occurred.", exc_info=True)
            output_context.exit_code = 102

        finally:
            output_context.output_properties['productName'] = self.title
            output_context.output_properties['brand'] = self.brand

        return output_context

    def abort(self) -> None:
        # Here, write your abort logic
        logger.debug("Abort requested")
        sys.exit(104)

