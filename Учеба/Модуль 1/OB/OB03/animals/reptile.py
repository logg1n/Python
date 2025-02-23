from .animal import Animal


class Reptile(Animal):
    def __init__(self, name, age, scales_color):
        super().__init__(name, age, scales_color)
        self.scales_color = scales_color

    def make_sound(self):
        print("Hiss")

    def eat(self):
        print(f"{self.name} is swallowing its prey whole.")

    def crawl(self):
        print(f"{self.name} is crawling with {self.scales_color} scales.")

    def __repr__(self):
        return f"{super().__repr__()}, Scale Color: {self.scales_color}"
