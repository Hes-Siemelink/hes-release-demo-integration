import logging

from digitalai.release.integration import BaseTask
from digitalai.release.v1.api.task_api import TaskApi
from digitalai.release.v1.model.flag_status import FlagStatus
from digitalai.release.v1.model.task import Task

logger = logging.getLogger('Digitalai')


class UpdateFlag(BaseTask):
    """
        Sets the warning flag on a task by invoking the API.
    """

    def __init__(self, params):
        super().__init__()
        self.message = params['message']

    def execute(self) -> None:
        task_api = TaskApi(self.get_default_api_client())

        task: Task = task_api.get_task(self.get_task_id())

        task.flag_comment = self.message
        task.flag_status = FlagStatus("ATTENTION_NEEDED")

        task_api.update_task(task.id, task=task)

        self.add_comment(f"Task flag updated to \"{self.message}\"")

        self.set_error_message("Failing so you can see the flag")
        self.set_exit_code(1)


