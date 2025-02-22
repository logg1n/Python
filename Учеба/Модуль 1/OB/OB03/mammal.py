from animal import Animal


class Mammal(Animal):
    def __init__(self, name, age, fur_type):
        super().__init__(name, age)
        self.fur_type = fur_type

    def make_sound(self):
        print("Growl")

    def eat(self):
        print(f"{self.name} is chewing on food.")

    def run(self):
        print(f"{self.name} is running with {self.fur_type} fur.")

    def __repr__(self):
        return f"Bird {self.name} age = {self.age}"
