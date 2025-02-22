from abc import ABC, abstractmethod


class Employee(ABC):
    @abstractmethod
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def work(self):
        pass
