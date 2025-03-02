from abc import ABC, abstractmethod
from typing import Dict

from .bag import Bag
from .items import Items


class Character(ABC):
    @abstractmethod
    def __init__(self, id: int, health: float, attack_power: float):
        self._id = id
        self.health: float = health
        self.attack_power: float = attack_power
        self._bag: Bag = None
        self._alive: bool = True

    @property
    def alive(self) -> bool:
        return self._alive

    @alive.setter
    def alive(self, value: bool):
        self._alive = value

    @property
    def bag(self) -> Bag:
        return self._bag

    @bag.setter
    def bag(self, value: Bag):
        self._bag = value

    @abstractmethod
    def attack(self) -> float:
        pass

    @abstractmethod
    def take_damage(self, attack_power: float):
        pass

    @abstractmethod
    def dead(self) -> Dict[int, Items] | None:
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        pass