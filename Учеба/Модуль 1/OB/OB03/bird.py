from animal import Animal


class Bird(Animal):
    def __init__(self, name, age, wing_span):
        super().__init__(name, age)
        self.wing_span = wing_span

    def make_sound(self):
        print("Chirp")

    def eat(self):
        print(f"{self.name} is pecking at seeds.")

    def fly(self):
        print(f"{self.name} is flying with a wingspan of {self.wing_span} meters.")

    def __repr__(self):
        return f"Bird {self.name} age = {self.age}"
