from time import sleep


class Hero:
   def __init__(self, name):
      self.name = name
      self.health = 100
      self.attack_power = 20

   def attack(self, other):
      other.health -= self.attack_power

   def is_alive(self):
      return self.health > 0


class Game:
   def __init__(self, player_name):
      self.player = Hero(player_name)
      self.computer = Hero("Компьютер")

   def start(self):
      print("Начинается битва героев!")
      while self.player.is_alive() and self.computer.is_alive():
         # Ход игрока
         print(f"\n{self.player.name} атакует {self.computer.name}!")
         self.player.attack(self.computer)
         print(f"Здоровье {self.computer.name}: {self.computer.health}")
         sleep(2)

         if not self.computer.is_alive():
            break

         # Ход компьютера
         print(f"\n{self.computer.name} атакует {self.player.name}!")
         self.computer.attack(self.player)
         print(f"Здоровье {self.player.name}: {self.player.health}")
         if not self.player.is_alive():
            break
         sleep(2)

      # Определение победителя
      if self.player.is_alive():
         print(f"\n{self.player.name} победил!")
      else:
         print(f"\n{self.computer.name} победил!")


if __name__ == "__main__":
   player_name = "Knight"
   game = Game(player_name)
   game.start()