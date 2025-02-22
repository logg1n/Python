from bird import Bird
from mammal import Mammal
from reptile import Reptile
from veterinarian import Veterinarian
from zoo import Zoo
from zookeeper import ZooKeeper


if __name__ == "__main__":
    zoo = Zoo()
    bird = Bird("Tweety", 1, 0.3)
    reptile = Reptile("Slinky", 2, "brown")
    mammal = Mammal("Fluffy", 3, "soft")
    zoo_keeper = ZooKeeper("Alice", 30)
    veterinarian = Veterinarian("Bob", 45)

    bird.make_sound()
    bird.eat()
    bird.fly()

    print()

    reptile.make_sound()
    reptile.eat()
    reptile.crawl()

    print()

    mammal.make_sound()
    mammal.eat()
    mammal.run()

    print()

    zoo_keeper.work()
    veterinarian.work()

    print()

    zoo.add_animal(bird)
    zoo.add_animal(mammal)
    zoo.add_animal(reptile)
    zoo.add_employee(veterinarian)
    zoo.add_employee(zoo_keeper)

    print(zoo)
