import logging
import sys

import requests
from datetime import datetime
from release_sdk import BaseTask, OutputContext, AbortException
from tenacity import wait_fixed, stop_after_attempt, Retrying, RetryError

logger = logging.getLogger(__name__)


class ExampleAbort(BaseTask):
    """ The developer should extend the BaseTask and override the 'exec' and 'abort' methods."""

    def __init__(self, param):
        self.aborted = False
        self.param = param

    def exec(self) -> OutputContext:
        """ Here is the task logic. It should return 'OutputContext' object. """

        output_context: OutputContext = OutputContext(-1, {}, [])
        logger.debug(f"Task property values are  : {self.param}")

        try:
            request_url = self.param['url'] + self.param['username'] + "/" + self.param['password']

            # Here, we wait for 'retry_waiting_time' seconds before attempting to retry and
            # we retry for 'max_retry_attempts' times.

            retryer = Retrying(wait=wait_fixed(self.param['retryWaitingTime']),
                               stop=stop_after_attempt(self.param['retryCount']))

            retryer(self.authenticate_user, request_url)
            self.__add_comment__("The user authentication was successful.")
            output_context.exit_code = 0

        except RetryError:
            self.__add_comment__("The user authentication was a failure.")
            output_context.exit_code = 0  # for task success

        except AbortException:
            self.handle_abort()

        except Exception:
            logger.error("Unexpected error occurred.", exc_info=True)
            output_context.exit_code = 102

        finally:
            output_context.output_properties['attemptNumber'] = retryer.statistics['attempt_number']

        return output_context

    def authenticate_user(self, request_url):
        response = requests.get(request_url)
        logger.debug(f"Status code : {response.status_code}, Datetime : {datetime.now()}")
        if self.is_aborted():
            raise AbortException()
        else:
            response.raise_for_status()

    def abort(self) -> None:
        self.aborted = True

    def is_aborted(self):
        return self.aborted

    def handle_abort(self) -> None:
        # Write your abort logic
        logger.debug("Abort requested")
        sys.exit(104)

    def __add_comment__(self, comment: str) -> None:
        logger.debug(f"##[start: comment]{comment}##[end: comment]")
