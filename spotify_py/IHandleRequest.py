from abc import ABC, abstractmethod
from typing import Self


class Success(str): pass
class Partial(str): pass
class Failure(str): pass

class IHandleRequest(ABC):
    def __init__(self):
        self.result: Success|Partial|Failure = None
        self.error: str = None

    @abstractmethod
    def Handle() -> Self:
        pass

    @abstractmethod
    def Result(self, print=True) -> Success|Partial|Failure:
        pass