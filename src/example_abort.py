import logging
import sys
import requests
from digitalai.release.container import BaseTask, AbortException
from tenacity import Retrying, RetryError, wait_fixed, stop_after_attempt

logger = logging.getLogger('Digitalai')


class ExampleAbort(BaseTask):
    """
    This class represents a task that demonstrates handling of abortion requests and retries.
    """

    def __init__(self, params):
        """
        Initializes the task with the given parameters.
        """
        super().__init__()
        self.aborted = False
        self.params = params
        self.server = params['server']

    def execute(self) -> None:
        """
        Executes the task. It first logs the task properties and then tries to authenticate the user using the
        `authenticate_user` method. If the authentication is successful, it updates the output properties with the
        status code of the response. If an abortion request is received, it handles it using the `handle_abort`
        method. If a `RetryError` or any other exception is raised, it logs the error and sets the exit code to 1.
        """
        logger.debug(f"Task property values are  : {self.params}")
        try:
            retryer = Retrying(wait=wait_fixed(self.params.get('retryWaitingTime')),
                               stop=stop_after_attempt(self.params.get('retryCount')),
                               after=self.update_status)

            response = retryer(self.authenticate_user)
            self.add_comment("The user authentication was successful.")
            output_properties = self.get_output_properties()
            output_properties['statusCode'] = response.status_code

        except RetryError:
            logger.error("The user authentication was a failure.", exc_info=True)
            self.set_exit_code(1)

        except AbortException:
            self.handle_abort()

        except Exception:
            logger.error("Unexpected error occurred.", exc_info=True)
            self.set_exit_code(1)

    def authenticate_user(self) -> requests.Response:
        """
        Sends a GET request to the '/basic-auth/user/login' endpoint of the server specified in the task parameters.

        Returns:
        - requests.Response: The response to the request.
        """
        base_url = self.server.get('url')
        context = '/basic-auth/user/login'
        url = base_url + context
        if self.params.get('username') and self.params.get('password'):
            auth = (self.params.get('username'), self.params.get('password'))
        else:
            auth = (self.server.get('username'), self.server.get('password'))
        response = requests.get(url, auth=auth)
        logger.debug(f"Status code : {response.status_code}")
        if self.is_aborted():
            raise AbortException()
        else:
            response.raise_for_status()
        return response

    def update_status(self, retry_state: object) -> None:
        """Update the status line with the current attempt number.

        Args:
            retry_state: An object that contains information about the current
                state of the task, including the attempt number.
        """
        status = f"Retrying: {retry_state.attempt_number}"
        self.set_status_line(status)

    def abort(self) -> None:
        """Set the `aborted` attribute to True to indicate that the task has been requested to be aborted."""
        self.aborted = True

    def is_aborted(self) -> bool:
        """Return the value of the `aborted` attribute.

        Returns:
            bool: The value of the `aborted` attribute.
        """
        return self.aborted

    def handle_abort(self) -> None:
        """Handle the request to abort the task.

        This method is called when the task has been requested to be
        aborted. It sets the exit code to 1 and exits the program.
        """
        logger.debug("Abort requested")
        self.set_exit_code(1)
        sys.exit(1)

