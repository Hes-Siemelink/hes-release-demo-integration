import logging
import requests
from digitalai.release.api.v1 import Configuration, ApiClient
from digitalai.release.api.v1.api.configuration_api import ConfigurationApi
from digitalai.release.api.v1.api.release_api import ReleaseApi
from digitalai.release.integration import BaseTask

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

            # For Release API testing

            release_server_url = self.get_release_server_url()
            if not release_server_url:
                release_server_url = "http://host.docker.internal:5516"

            task_user = self.get_task_user();
            if not task_user.username:
                task_user.username = 'admin'
                task_user.password = 'admin'

            configuration = Configuration(host=release_server_url, username=task_user.username, password=task_user.password)
            api_client = ApiClient(configuration)

            configuration_api = ConfigurationApi(api_client)
            response_api = configuration_api.get_global_variables()
            print(f"get_global_variables : {response_api}\n")

            release_api = ReleaseApi(api_client)
            response_api = release_api.get_releases(depth=1, page=0, results_per_page=1)
            print(f"get_releases : {response_api}\n")


        except Exception as e:
            logger.error("Unexpected error occurred.", exc_info=True)
            self.set_exit_code(1)
            self.set_error_message(str(e))
        finally:
            self.set_output_property('textValue',self.textValue)
