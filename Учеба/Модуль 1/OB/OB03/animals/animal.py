from abc import ABC, abstractmethod
import json


class Animal(ABC):
    @abstractmethod
    def __init__(self, name, age, param):
        self.name = name
        self.age = age
        self.unique_param = param

    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def eat(self):
        pass

    def get_info(self) -> str:
        return json.dumps(
            {
                "type": self.__class__.__name__,
                "name": self.name,
                "age": self.age,
                "unique_param": str(self.unique_param),
            }
        )

    def set_info(self, info):
        return json.loads(info)

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.name}, Age: {self.age}"
