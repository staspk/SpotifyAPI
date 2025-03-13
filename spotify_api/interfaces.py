from abc import ABC, abstractmethod
from typing import Self, Union


class Success():
    pass

class PartialSuccess():
    description:str

    def __init__(self, description:str = ""):
        self.description = description

class ErrorMsg():
    message: str

    def __init__(self, message: str):
        if message is None:
            raise ValueError('message cannot be none in ErrorMsg init')
        self.message = message
    
    def __str__(self):
        return self.message


class IHandleRequest(ABC):
    result: any = None
    errorMsg: ErrorMsg = None

    @abstractmethod
    def Handle() -> Self:
        pass

    @abstractmethod
    def Result(self, print=False) -> Union[any, ErrorMsg]:
        pass