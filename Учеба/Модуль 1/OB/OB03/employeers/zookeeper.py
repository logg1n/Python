from .employee import Employee


class ZooKeeper(Employee):
    def __init__(self, name, age):
        super().__init__(name, age)

    def work(self):
        print(f"{self.name} is feeding the animals.")
