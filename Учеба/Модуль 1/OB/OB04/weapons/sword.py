from abc import ABC, abstractmethod
from .weapon import Weapon

class Sword(Weapon):
   def __init__(self,id: int, attack_power: float):
      super().__init__(id, attack_power)
