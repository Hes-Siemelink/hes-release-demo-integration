import logging
import time

from digitalai.release.integration import BaseTask

logger = logging.getLogger('Digitalai')


class Hello(BaseTask):

    def __init__(self, params):
        super().__init__()
        self.params = params
        self.greeting = None

    def execute(self) -> None:
        try:
            name = self.params['yourName']
            if not name:
                raise ValueError("Your Name field cannot be empty")
            self.greeting = f"Hello {name}"
            # Testing : Loop 10 times with a 3 second pause between iterations
            for i in range(10):
                print(f"Iteration {i + 1}")
                time.sleep(3)
        except Exception as e:
            logger.error("Unexpected error occurred.", exc_info=True)
            self.set_exit_code(1)
            self.set_error_message(str(e))
        finally:
            output_properties = self.get_output_properties()
            output_properties["greeting"] = self.greeting
