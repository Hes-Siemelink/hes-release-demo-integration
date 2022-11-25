import logging
import sys

import requests
from datetime import datetime

from release_sdk import BaseTask, OutputContext, AbortException
from tenacity import wait_fixed, stop_after_attempt, Retrying, retry_if_exception_type

logger = logging.getLogger(__name__)


class ExampleAbort(BaseTask):
    """ The developer should extend the BaseTask and override the 'exec' and 'abort' methods."""

    def __init__(self, param):
        self.aborted = False
        self.param = param

    def exec(self) -> OutputContext:
        """ Here is the task logic. It should return 'OutputContext' object. """

        output_context: OutputContext = OutputContext(-1, {}, [])
        print(f"Task property values are  : {self.param}")
        logger.debug(f"Task property values are  : {self.param}")

        try:
            request_url = self.param['url'] + self.param['username'] + "/" + self.param['password']

            # Here, we wait for 'retry_waiting_time' seconds before attempting to retry and
            # we retry for 'max_retry_attempts' times.
            # It will retry in case of RuntimeError

            retryer = Retrying(wait=wait_fixed(self.param['retryWaitingTime']),
                               stop=stop_after_attempt(self.param['retryCount']),
                               retry=retry_if_exception_type(RuntimeError))

            retryer(self.authenticate_user, request_url)

            output_context.exit_code = 0

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
        if response.status_code != 200:
            if self.is_aborted():
                raise AbortException()
            else:
                raise RuntimeError()

    def abort(self) -> None:
        self.aborted = True

    def is_aborted(self):
        return self.aborted

    def handle_abort(self) -> None:
        # Write your abort logic
        logger.debug("Abort requested")
        sys.exit(104)
