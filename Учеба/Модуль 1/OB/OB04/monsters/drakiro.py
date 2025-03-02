from typing import Dict

from .monster import Monster
from interfaces import Items

class Drakiro(Monster):
   def __init__(self,id, health: float, attack_power: float):
      super().__init__(id, health, attack_power)

   def attack(self) -> float:
      print(f"{self.__class__.__name__} выпускает поток огня!")
      return self.attack_power

   def take_damage(self, attack_power: float):
      self.health -= attack_power
      print(f"{self.__class__.__name__} получает урон {attack_power}. Оставшееся здоровье: {self.health}")

   def dead(self) -> Dict[int, Items]:
      print(f"{self.__class__.__name__} падает в куче пепла.")
      return self.bag.lose_items()

   def is_alive(self) -> bool:
      if self.health <= 0:
         self.alive = False

      return self.alive
