from abc import abstractmethod
from interfaces import Character


class Monster(Character):
   @abstractmethod
   def __init__(self,id, health: float, attack_power: float,):
      super().__init__(id, health, attack_power,)

   @abstractmethod
   def attack(self) -> float:
      pass

   @abstractmethod
   def take_damage(self, attack_power: float):
      pass

   @abstractmethod
   def dead(self):
      pass

   @abstractmethod
   def is_alive(self) -> bool:
      pass