from abc import ABC, abstractmethod
from typing import Self
from kozubenko.string import labeledStr


class Success(labeledStr): pass
class Partial(labeledStr): pass
class Failure(labeledStr): pass

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