import logging
import requests
from digitalai.release.container import BaseTask

logger = logging.getLogger('Digitalai')


class DummyJson(BaseTask):

    def __init__(self, params):
        super().__init__()
        self.params = params
        self.server = params['server']
        self.server_url = self.server['url'].strip("/")
        self.auth = (self.server['username'], self.server['password'])
        self.product_id = self.params['productId']
        self.product_name = None
        self.product_brand = None

    def execute(self) -> None:
        try:
            request_url = self.server_url + "/products/" + self.product_id
            self.add_comment(f"Request URL is {request_url}")
            response = requests.get(request_url, auth=self.auth)
            response.raise_for_status()
            self.product_name = response.json()['title'].strip()
            self.product_brand = response.json()['brand'].strip()
        except Exception as e:
            logger.error("Unexpected error occurred.", exc_info=True)
            self.set_exit_code(1)
            self.set_error_message(str(e))
        finally:
            output_properties = self.get_output_properties()
            output_properties['productName'] = self.product_name
            output_properties['productBrand'] = self.product_brand
