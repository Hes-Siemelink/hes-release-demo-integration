import logging
import requests
from digitalai.release.integration import BaseTask

logger = logging.getLogger('Digitalai')


class Base64Decode(BaseTask):

    def __init__(self, params):
        super().__init__()
        self.params = params
        self.textValue = None

    def execute(self) -> None:
        try:
            base64_value = self.params['base64Value']
            response = requests.get(f'https://httpbin.org/base64/{base64_value}')
            response.raise_for_status()
            if 'Incorrect Base64 data' in response.text:
                raise ValueError(response.text)
            self.textValue = response.text
        except Exception as e:
            logger.error("Unexpected error occurred.", exc_info=True)
            self.set_exit_code(1)
            self.set_error_message(str(e))
        finally:
            output_properties = self.get_output_properties()
            output_properties["textValue"] = self.textValue
