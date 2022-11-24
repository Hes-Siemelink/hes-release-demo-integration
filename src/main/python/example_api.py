import logging

import requests
from release_sdk import BaseTask, OutputContext, AbortException

logger = logging.getLogger(__name__)


class ExampleApi(BaseTask):
    def __init__(self, param):
        self.param = param
        self.task_id = param['task_id']

    def exec(self) -> OutputContext:
        output_context: OutputContext = OutputContext(-1, {}, [])
        url = self.param['url']+self.param['productId']
        self.__add_comment__(f"Request URL is {url}")
        response = requests.get(url)
        response_json = response.json()

        output_context.output_properties['productName'] = response_json['title']
        output_context.output_properties['brand'] = response_json['brand']
        output_context.exit_code = 0

        return output_context

    def abort(self) -> None:
        raise AbortException

    def __add_comment__(self, comment: str) -> None:
        logger.debug(f"##[start: comment]{comment}##[end: comment]")


