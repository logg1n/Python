from .weapon import Weapon


class Bow(Weapon):
   def __init__(self,id: int, attack_power: float):
      super().__init__(id, attack_power)
