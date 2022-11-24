import logging
import sys
from abc import ABC, abstractmethod
from .output_context import OutputContext


class BaseTask(ABC):

    @abstractmethod
    def exec(self) -> OutputContext:
        pass

    @abstractmethod
    def abort(self) -> None:
        pass

