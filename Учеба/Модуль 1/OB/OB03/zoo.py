from animal import Animal
from employee import Employee


class Zoo:
    def __init__(self):
        self.animals = []
        self.employees = []

    def add_animal(self, animal: Animal):
        self.animals.append(animal)

    def add_employee(self, employee: Employee):
        self.employees.append(employee)

    def __repr__(self):
        return (
            f"Zoo have {len(self.animals)} animals and {len(self.employees)} Employees"
        )
