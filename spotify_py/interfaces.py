from abc import ABC, abstractmethod
from typing import Self, Union


class Success():
    def __str__(self):
        return 'Success'

class PartialSuccess():
    def __init__(self, description:str = ''):
        self.description = description

    def __str__(self):
        return f'Partial Success: {self.description}'

class ErrorMsg():
    def __init__(self, message: str):
        self.message = message
    
    def __str__(self):
        return f'ErrorMsg: {self.message}'


class IHandleRequest(ABC):
    def __init__(self):
        self.result: any = None
        self.errorMsg: ErrorMsg = None

    @abstractmethod
    def Handle() -> Self:
        pass

    @abstractmethod
    def Result(self, print=False) -> Union[any, ErrorMsg]:
        pass