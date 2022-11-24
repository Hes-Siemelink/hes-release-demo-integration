import json
import os
import sys

from .input_context import InputContext
from .job_data_encryptor import AESJobDataEncryptor, NoOpJobDataEncryptor
from .output_context import OutputContext
from .masked_io import MaskedIO


# masked IO
masked_std_out = MaskedIO(sys.stdout)
masked_std_err = MaskedIO(sys.stderr)
sys.stdout = masked_std_out
sys.stderr = masked_std_err

# input and output context file location
input_context_file = os.getenv('INPUT_LOCATION', '/input')
output_context_file = os.getenv('OUTPUT_LOCATION', '/output')
base64_session_key = os.getenv('SESSION_KEY', '')
encryptor = AESJobDataEncryptor(base64_session_key) if base64_session_key else NoOpJobDataEncryptor()


class BasePlugin:

    def __init__(self):
        self.output_context = OutputContext(-1, {}, [])
        self.task_object = None

    def get_task_properties(self):
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

    def execute_job(self) -> None:
        self.output_context = self.task_object.exec()

    def create_output_context_file(self):
        with open(output_context_file, "w") as data_output:
            output_content = json.dumps(self.output_context.to_dict())
            encrypted_json = encryptor.encrypt(output_content)
            data_output.write(encrypted_json)

    def abort_job(self):
        if self.task_object:
            self.task_object.abort()
        else:
            sys.exit(104)
