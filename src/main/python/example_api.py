import logging
import requests
from dai_release_sdk import BaseTask

logger = logging.getLogger('DAI')


class ExampleApi(BaseTask):

    def __init__(self, params):
        super().__init__()
        self.params = params

    def execute(self) -> None:
        logger.debug(f"Task property values are  : {self.params}")
        try:
            request_url = "https://dummyjson.com/products/" + self.params['productId']
            self.add_comment(f"Request URL is {request_url}")
            response = requests.get(request_url)
            response.raise_for_status()
            output_properties = self.get_output_properties()
            output_properties['productName'] = response.json()['title']
            output_properties['brand'] = response.json()['brand']

        except Exception:
            logger.error("Unexpected error occurred.", exc_info=True)
            self.set_exit_code(1)
