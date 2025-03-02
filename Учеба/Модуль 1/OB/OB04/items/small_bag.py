from interfaces import Bag


class SmallBag(Bag):
   def __init__(self, capacity: int = 5):
      super().__init__(capacity)

