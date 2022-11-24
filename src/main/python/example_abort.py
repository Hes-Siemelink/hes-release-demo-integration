import logging
import time

from release_sdk import BaseTask, OutputContext, AbortException

logger = logging.getLogger(__name__)


class ExampleAbort(BaseTask):

    def __init__(self, param):
        self.aborted = False
        self.param = param

    def exec(self) -> OutputContext:
        output_context: OutputContext = OutputContext(-1, {}, [])
        loop_count = self.param['loopCount']
        wait_time = self.param['waitTime']

        for x in range(loop_count):
            if self.is_aborted():
                self.handle_abort()
            logger.debug(f"This prints once a {wait_time} seconds and count value is {x + 1}")
            time.sleep(wait_time)

        output_context.exit_code = 0
        return output_context

    def abort(self) -> None:
        self.aborted = True

    def is_aborted(self):
        return self.aborted

    def handle_abort(self) -> None:
        # Write your abort logic and raise the AbortException
        raise AbortException
