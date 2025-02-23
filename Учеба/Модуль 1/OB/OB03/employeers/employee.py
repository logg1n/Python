from abc import ABC, abstractmethod
import json


class Employee(ABC):
    @abstractmethod
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def work(self):
        pass

    def get_info(self) -> str:
        return json.dumps(
            {
                "type": self.__class__.__name__,
                "name": self.name,
                "age": self.age,
            }
        )

    def set_info(self, info):
        return json.loads(info)

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.name}, Age: {self.age}"
