from abc import abstractmethod
from typing import Dict

from interfaces import Character, Items
from weapons import Weapon

class Fighter(Character):
   @abstractmethod
   def __init__(self,id: int, health: float, attack_power: float, defense: float):
      super().__init__(id, health, attack_power)
      self.defense: float = defense
      self._weapon = None

   @property
   def weapon(self):
      return self._weapon

   @weapon.setter
   def weapon(self, value):
      self._weapon = value

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

   @abstractmethod
   def take_prize(self, items: Dict[int, Items]):
      pass