from interfaces import Items


class Weapon(Items):
   def __init__(self,id: int, attack_power: float):
      super().__init__(id)
      self.attack_power: float = attack_power