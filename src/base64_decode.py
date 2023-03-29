import logging
import requests
from digitalai.release.integration import BaseTask
from digitalai.release.v1 import Configuration, ApiClient
from digitalai.release.v1.api.configuration_api import ConfigurationApi
from digitalai.release.v1.api.release_api import ReleaseApi
from digitalai.release.v1.model.release import Release
from digitalai.release.v1.model.system_message_settings import SystemMessageSettings
from digitalai.release.v1.model.variable import Variable

logger = logging.getLogger('Digitalai')


class Base64Decode(BaseTask):
    """
        The purpose of this task is to decode the base64 value.
    """

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
            self.set_output_property('textValue', self.textValue)
