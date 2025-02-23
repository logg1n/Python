from .animal import Animal


class Bird(Animal):
    def __init__(self, name, age: float, wing_span: float):
        super().__init__(name, age, wing_span)
        self.wing_span = wing_span

    def make_sound(self):
        print("Chirp")

    def eat(self):
        print(f"{self.name} is pecking at seeds.")

    def fly(self):
        print(f"{self.name} is flying with a wingspan of {self.wing_span} meters.")

    def __repr__(self):
        return f"{super().__repr__()}, Wing Span: {self.wing_span}"
