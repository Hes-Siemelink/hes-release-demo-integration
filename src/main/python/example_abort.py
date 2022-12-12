import logging
import sys

from datetime import datetime
from dai_release_sdk import BaseTask, AbortException, HttpRequest
from requests import Response
from tenacity import wait_fixed, stop_after_attempt, Retrying, RetryError

logger = logging.getLogger('DAI')


class ExampleAbort(BaseTask):

    def __init__(self, params):
        self.aborted = False
        self.params = params
        self.request = HttpRequest(params['server'], params['username'], params['password'])

    def execute(self) -> None:
        logger.debug(f"Task property values are  : {self.params}")
        try:
            # Here, we wait for 'retry_waiting_time' seconds before attempting to retry
            # we retry for 'max_retry_attempts' times.

            retryer = Retrying(wait=wait_fixed(self.params['retryWaitingTime']),
                               stop=stop_after_attempt(self.params['retryCount']),
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

    def authenticate_user(self) -> Response:
        response = self.request.do_request(method='GET', context='/basic-auth/user/login')
        logger.debug(f"Status code : {response.status_code}, Datetime : {datetime.now()}")
        if self.is_aborted():
            raise AbortException()
        else:
            response.raise_for_status()
        return response

    def update_status(self, retry_state) -> None:
        status = f"Retrying: {retry_state.attempt_number}"
        self.set_status_line(status)

    def abort(self) -> None:
        self.aborted = True

    def is_aborted(self) -> bool:
        return self.aborted

    def handle_abort(self) -> None:
        # Here, write your abort logic
        logger.debug("Abort requested")
        self.set_exit_code(1)
        sys.exit(1)
