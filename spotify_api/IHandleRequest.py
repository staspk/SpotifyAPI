from abc import ABC, abstractmethod
from typing import Self, Union


class ErrorMsg():
    message: str

    def __init__(self, message: str):
        if message is None:
            raise ValueError('message cannot be none in ErrorMsg init')
        self.message = message
    
    def __str__(self):
        self.message


class IHandleRequest(ABC):
    result: any = None
    errorMsg: ErrorMsg = None

    @abstractmethod
    def Handle() -> Self:
        pass

    @abstractmethod
    def Result(self, print=False) -> Union[any, ErrorMsg]:
        pass