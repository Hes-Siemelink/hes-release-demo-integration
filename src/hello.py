import logging

from digitalai.release.integration import BaseTask

logger = logging.getLogger('Digitalai')


class Hello(BaseTask):
    """
       The purpose of this task is to greet by the given name.
    """
    def __init__(self, params):
        super().__init__()
        self.params = params
        self.greeting = None

    def execute(self) -> None:
        try:
            name = self.params['yourName']
            if not name:
                raise ValueError("The Name field cannot be empty")
            self.greeting = f"Hello {name}"
            self.add_comment(self.greeting)

        except Exception as e:
            logger.error("Unexpected error occurred.", exc_info=True)
            self.set_exit_code(1)
            self.set_error_message(str(e))
        finally:
            output_properties = self.get_output_properties()
            output_properties["greeting"] = self.greeting
