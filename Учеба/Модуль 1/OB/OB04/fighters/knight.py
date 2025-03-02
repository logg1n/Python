from typing import Dict

from .fighter import Fighter
from interfaces import Items

class Knight(Fighter):
   def __init__(self,id, health: float, defense: float, attack_power : float = 5):
      super().__init__(id, health, attack_power, defense)

   def attack(self) -> float:
      print(f"{self.__class__.__name__} атакует с {self.weapon.__class__.__name__}!")
      return self.attack_power + self.weapon.attack_power

   def take_damage(self, attack_power: float):
      effective_attack_power = max(attack_power - self.defense, 0)
      self.health -= effective_attack_power
      print(f"{self.__class__.__name__} получает урон {effective_attack_power}. Оставшееся здоровье: {self.health}")

   def dead(self) -> Dict[int, Items] | None:
      print(f"{self.__class__.__name__} пал в бою.")
      return self.bag.lose_items()

   def is_alive(self) -> bool:
      if self.health <= 0:
         self.alive = False

      return self.alive

   def take_prize(self, items: Dict[int, Items]):
      for v in items.values():
         self.bag.put(v)