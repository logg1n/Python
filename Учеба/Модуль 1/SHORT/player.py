class Player:
   def __init__(self):
      """Пустой конструктор."""
      self.id = None
      self.name = None
      self.total_wins = None
      self.total_lose = None
      self._sym = None

   def initialize(self, *args):
      """
      Универсальный метод для инициализации свойств игрока.
      :param args: Либо только имя (строка), либо данные (кортеж или список).
      """
      if len(args) == 1 and isinstance(args[0], str):
         # Инициализация только с именем
         self.name = args[0]
         self.total_wins = 0
         self.total_lose = 0
      elif len(args) == 1 and isinstance(args[0], (list, tuple)):
         # Инициализация из кортежа или списка
         data = args[0]
         self.name = data[1]
         self.total_wins = data[2] if len(data) > 1 else 0
         self.total_lose = data[3] if len(data) > 2 else 0
      else:
         raise ValueError("Некорректные данные для инициализации")

   @property
   def sym(self):
      """Геттер для sym."""
      return self._sym

   @sym.setter
   def sym(self, value):
      """Сеттер для sym."""
      self._sym = value

   def __str__(self):
      """Отображение объекта в строковом формате."""
      return (f"{self.name} -  "
              f"W:{self.total_wins}, L: {self.total_lose} ")

