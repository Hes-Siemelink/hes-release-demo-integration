from digitalai.release.integration import BaseTask


class Hello(BaseTask):
    """
       The purpose of this task is to greet by the given name.
    """
    def __init__(self, params):
        super().__init__()
        self.params = params

    def execute(self) -> None:
        name = self.params['yourName']
        if not name:
            raise ValueError("The 'name' field cannot be empty")

        greeting = f"Hello {name}"

        # Add to the comment section of the task in the UI
        self.add_comment(greeting)

        self.set_output_property('greeting', greeting)

