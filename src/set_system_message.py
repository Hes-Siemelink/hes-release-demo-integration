import logging

from digitalai.release.integration import BaseTask
from digitalai.release.v1 import Configuration, ApiClient
from digitalai.release.v1.api.configuration_api import ConfigurationApi
from digitalai.release.v1.model.system_message_settings import SystemMessageSettings

logger = logging.getLogger('Digitalai')


class SetSystemMessage(BaseTask):
    """
        Sets the system message in the Release UI by invoking the API.
    """

    def __init__(self, params):
        super().__init__()
        self.message = params['message']

    def execute(self) -> None:
        try:
            # For Release API methods testing

            # release_server_url = self.get_release_server_url()
            # if not release_server_url:
            #     release_server_url = "http://host.docker.internal:5516"

            # task_user = self.get_task_user()
            # if not task_user.username:
            #     task_user.username = 'admin'
            #     task_user.password = 'admin'

            # self.add_comment(f"Release URL: `{self.get_release_server_url()}`  \nUser name: `{self.get_task_user()}`")

            configuration = Configuration(
                # host=self.get_release_server_url(),
                host="http://host.docker.internal:5516",
                username=self.get_task_user().username,
                password=self.get_task_user().password)
            api_client = ApiClient(configuration)
            configuration_api = ConfigurationApi(api_client)

            system_message = SystemMessageSettings(
                message=self.message,
                type='xlrelease.SystemMessageSettings',
                id='Configuration/settings/SystemMessageSettings',
                enabled=True,
                automated=False
            )

            configuration_api.update_system_message(system_message_settings=system_message)

            self.add_comment(f"System message updated to {self.message}")

        except Exception as e:
            logger.error("Unexpected error occurred.", exc_info=True)
            self.set_exit_code(1)
            self.set_error_message(str(e))
