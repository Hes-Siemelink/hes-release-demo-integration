import logging
import sys

import requests

from dai_release_sdk import BaseTask, OutputContext

logger = logging.getLogger(__name__)


class ExampleApi(BaseTask):
    """ The developer should extend the BaseTask and override the 'exec' and 'abort' methods."""

    def __init__(self, params):
        self.params = params

    def exec(self) -> OutputContext:
        """ Here is the task logic. It should return 'OutputContext' object. """

        output_context: OutputContext = OutputContext(-1, {}, [])
        logger.debug(f"Task property values are  : {self.params}")

        try:
            request_url = "https://dummyjson.com/products/" + self.params['productId']
            self.__add_comment__(f"Request URL is {request_url}")
            response = requests.get(request_url)
            response.raise_for_status()

            output_context.output_properties['productName'] = response.json()['title']
            output_context.output_properties['brand'] = response.json()['brand']
            output_context.exit_code = 0

        except Exception:
            logger.error("Unexpected error occurred.", exc_info=True)

        return output_context

    def abort(self) -> None:
        sys.exit(1)

