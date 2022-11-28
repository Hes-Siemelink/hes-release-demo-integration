import json
import os
import sys

from .input_context import InputContext
from .job_data_encryptor import AESJobDataEncryptor, NoOpJobDataEncryptor
from .output_context import OutputContext
from .masked_io import MaskedIO

# masked IO
masked_std_out: MaskedIO = MaskedIO(sys.stdout)
masked_std_err: MaskedIO = MaskedIO(sys.stderr)
sys.stdout = masked_std_out
sys.stderr = masked_std_err

# input and output context file location
input_context_file: str = os.getenv('INPUT_LOCATION', '/input')
output_context_file: str = os.getenv('OUTPUT_LOCATION', '/output')
base64_session_key: str = os.getenv('SESSION_KEY', '')
encryptor = AESJobDataEncryptor(base64_session_key) if base64_session_key else NoOpJobDataEncryptor()


def get_task_properties():
    with open(input_context_file) as data_input:
        input_content = data_input.read()
        decrypted_json = encryptor.decrypt(input_content)
        input_context = InputContext.from_dict(json.loads(decrypted_json))
    secrets = input_context.task.secrets()
    masked_std_out.secrets = secrets
    masked_std_err.secrets = secrets
    task_properties = input_context.task.build_locals()
    task_properties['task_id'] = input_context.task.id
    return task_properties


def create_output_context_file(output_context: OutputContext):
    with open(output_context_file, "w") as data_output:
        output_content = json.dumps(output_context.to_dict())
        encrypted_json = encryptor.encrypt(output_content)
        data_output.write(encrypted_json)


class BasePlugin:

    def __init__(self):
        self.task_object: None = None

    def execute_job(self) -> OutputContext:
        if self.task_object:
            return self.task_object.exec()
        else:
            raise ValueError("task_object is None")

    def abort_job(self):
        if self.task_object:
            self.task_object.abort()
        else:
            sys.exit(104)
