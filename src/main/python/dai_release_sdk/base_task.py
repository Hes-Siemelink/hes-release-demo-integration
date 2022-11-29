import logging
from abc import ABC, abstractmethod
from .output_context import OutputContext


class BaseTask(ABC):

    @abstractmethod
    def exec(self) -> OutputContext:
        pass

    @abstractmethod
    def abort(self) -> None:
        pass

    def __add_comment__(self, logger: logging.Logger, comment: str) -> None:
        logger.debug(f"##[start: comment]{comment}##[end: comment]")

    def __set_status_line__(self, logger: logging.Logger, status_line: str) -> None:
        logger.info(f"##[start: status]{status_line}##[end: status]")

