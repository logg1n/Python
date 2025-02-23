from .employee import Employee


class Veterinarian(Employee):
    def __init__(self, name, age: float):
        super().__init__(name, age)

    def work(self):
        print(f"{self.name} is healing the animals.")
