from abc import ABC, abstractmethod

class Items(ABC):
    @abstractmethod
    def __init__(self, id: int):
        self._id = id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value
