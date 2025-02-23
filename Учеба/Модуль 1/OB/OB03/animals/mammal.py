from .animal import Animal


class Mammal(Animal):
    def __init__(self, name, age: float, fur_type):
        super().__init__(name, age, fur_type)
        self.fur_type = fur_type

    def make_sound(self):
        print("Growl")

    def eat(self):
        print(f"{self.name} is chewing on food.")

    def run(self):
        print(f"{self.name} is running with {self.fur_type} fur.")

    def __repr__(self):
        return f"{super().__repr__()}, Fur Type: {self.fur_type}"
