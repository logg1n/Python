import json
from typing import Dict
from animals import Animal, Bird, Reptile, Mammal
from employeers import Employee, Veterinarian, ZooKeeper


class Zoo:
    def __init__(self):
        self.animals = []
        self.employees = []

    def add_animal(self, animal: Animal):
        self.animals.append(animal)

    def add_employee(self, employee: Employee):
        self.employees.append(employee)

    def pretty_print_list(self, items):
        print("Список элементов:")
        print("===================")
        for index, item in enumerate(items, start=1):
            print(f"{index}. {item}")
        print("===================")

    def get_animals(self):
        self.pretty_print_list(self.animals)

    def get_employees(self):
        self.pretty_print_list(self.employees)

    # -------------------------------------------------------------------------
    # {type: ,name: ,age: ,unique_pqram}
    def set_info(self, data: Dict[int, Dict]):
        for v in data.values():
            t = json.loads(v)
            type_a: str = t["type"]

            match type_a:
                case "Bird":
                    bird = Bird(t["name"], t["age"], t["unique_param"])
                    self.add_animal(bird)
                case "Mammal":
                    mammal = Mammal(t["name"], t["age"], t["unique_param"])
                    self.add_animal(mammal)
                case "Reptile":
                    reptile = Reptile(t["name"], t["age"], t["unique_param"])
                    self.add_animal(reptile)
                case "Veterinarian":
                    veterinarian = Veterinarian(t["name"], t["age"])
                    self.add_employee(veterinarian)
                case "ZooKeeper":
                    zoo_keeper = ZooKeeper(t["name"], t["age"])
                    self.add_employee(zoo_keeper)

    def get_info(self) -> str:
        book = {}
        for i, a in enumerate(self.animals + self.employees):
            a: Animal | Employee
            book.update({i: a.get_info()})

        return json.dumps(book)

    def __repr__(self):
        return (
            f"Zoo have {len(self.animals)} animals and {len(self.employees)} Employees"
        )
