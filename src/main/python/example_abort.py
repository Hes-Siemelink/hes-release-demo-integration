import logging
import sys


from datetime import datetime
from dai_release_sdk import BaseTask, OutputContext, AbortException, HttpRequest
from tenacity import wait_fixed, stop_after_attempt, Retrying, RetryError

logger = logging.getLogger(__name__)


class ExampleAbort(BaseTask):
    """ The developer should extend the BaseTask and override the 'exec' and 'abort' methods."""

    def __init__(self, params):
        self.aborted = False
        self.params = params
        self.request = HttpRequest(params['server'], params['username'], params['password'])

    def exec(self) -> OutputContext:
        """ Here is the task logic. It should return 'OutputContext' object. """

        output_context: OutputContext = OutputContext(-1, {}, [])
        logger.debug(f"Task property values are  : {self.params}")

        try:
            # Here, we wait for 'retry_waiting_time' seconds before attempting to retry
            # we retry for 'max_retry_attempts' times.

            retryer = Retrying(wait=wait_fixed(self.params['retryWaitingTime']),
                               stop=stop_after_attempt(self.params['retryCount']),
                               after=self.update_status)

            response = retryer(self.authenticate_user)
            self.__add_comment__("The user authentication was successful.")
            output_context.output_properties['statusCode'] = response.status_code
            output_context.exit_code = 0

        except RetryError:
            logger.error("The user authentication was a failure.", exc_info=True)

        except AbortException:
            self.handle_abort()

        except Exception:
            logger.error("Unexpected error occurred.", exc_info=True)

        return output_context

    def authenticate_user(self):
        response = self.request.do_request(method='GET', context='/basic-auth/user/login')
        logger.debug(f"Status code : {response.status_code}, Datetime : {datetime.now()}")
        if self.is_aborted():
            raise AbortException()
        else:
            response.raise_for_status()
        return response

    def update_status(self, retry_state):
        status = f"Retrying: {retry_state.attempt_number}"
        self.__set_status_line__(status)

    def abort(self) -> None:
        self.aborted = True

    def is_aborted(self):
        return self.aborted

    def handle_abort(self) -> None:
        # Here, write your abort logic
        logger.debug("Abort requested")
        sys.exit(1)


