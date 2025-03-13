from abc import ABC, abstractmethod
from typing import Self, Union


class ErrorMsg():
    message: str

    def __init__(self, message: str):
        if message is None:
            raise ValueError('message cannot be none in ErrorMsg init')
        self.message = message


class IHandleRequest(ABC):
    ErrorMsg: ErrorMsg

    @abstractmethod
    def Handle() -> Self:
        pass

    @abstractmethod
    def Result() -> Union[any, ErrorMsg]:
        pass