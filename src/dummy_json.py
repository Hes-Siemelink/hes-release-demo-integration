import logging
import requests
from digitalai.release.integration import BaseTask

logger = logging.getLogger('Digitalai')


class DummyJson(BaseTask):
    """
        The purpose of this task is to fetch product details from a remote server by product ID.
    """
    def __init__(self, params):
        super().__init__()
        self.params = params
        self.product_id = self.params['productId']
        self.product_name = None
        self.product_brand = None

    def execute(self) -> None:
        try:
            if not self.params['server']:
                raise ValueError("Server field cannot be empty")
            else:
                server = self.params['server']
            server_url = server['url'].strip("/")
            auth = (server['username'], server['password'])
            request_url = server_url + "/products/" + self.product_id
            self.add_comment(f"Request URL is {request_url}")
            response = requests.get(request_url, auth=auth)
            response.raise_for_status()
            self.product_name = response.json()['title'].strip()
            self.product_brand = response.json()['brand'].strip()
        except Exception as e:
            logger.error("Unexpected error occurred.", exc_info=True)
            self.set_exit_code(1)
            self.set_error_message(str(e))
        finally:
            self.set_output_property('productName', self.product_name)
            self.set_output_property('productBrand', self.product_brand)
