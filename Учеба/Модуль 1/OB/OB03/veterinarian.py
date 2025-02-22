from employee import Employee


class Veterinarian(Employee):
    def __init__(self, name, age):
        super().__init__(name, age)

    def work(self):
        print(f"{self.name} is healing the animals.")

    def __repr__(self):
        return f"{self.__class__.__name__} {self.name} age = {self.age}"
