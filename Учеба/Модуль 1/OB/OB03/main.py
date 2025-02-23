import os
from animals import Bird, Reptile, Mammal
from employeers import Veterinarian, ZooKeeper
from managers import Zoo, FileManager


if __name__ == "__main__":
    zoo = Zoo()
    execution_successful = True

    try:
        file_manager = FileManager("save", os.path.dirname(os.path.abspath(__file__)))
        data = file_manager.load()

        if isinstance(data, dict):
            zoo.set_info(data)
        else:
            zoo.set_info({})

        print("#################")
        print("#  Zoo Manager  #")
        print("#################")

        while True:
            answ = int(input("Menu\n1. Animals\n2. Employees\n3. Exit\n"))

            match answ:
                case 1:
                    a1 = int(input("1. Get Animals\n2. Add Animal\n"))
                    match a1:
                        case 1:
                            zoo.get_animals()
                        case 2:
                            a2 = int(
                                input(
                                    "Check classification:\n1. Bird\n2. Mammal\n3. Reptile\n"
                                )
                            )
                            match a2:
                                case 1:
                                    name = input("Write name: ")
                                    age = float(input("Write age: "))
                                    wing_span = float(input("Write wing span: "))
                                    bird = Bird(name, age, wing_span)
                                    zoo.add_animal(bird)
                                    print(f"\n{bird} -> Добавлен\n")
                                case 2:
                                    name = input("Write name: ")
                                    age = float(input("Write age: "))
                                    fur_type = input("Write fur type: ")
                                    mammal = Mammal(name, age, fur_type)
                                    zoo.add_animal(mammal)
                                    print(f"\n{mammal} -> Добавлен\n")
                                case 3:
                                    name = input("Write name: ")
                                    age = float(input("Write age: "))
                                    scales_color = input("Write scales color: ")
                                    reptile = Reptile(name, age, scales_color)
                                    zoo.add_animal(reptile)
                                    print(f"\n{reptile} -> Добавлен\n")
                case 2:
                    a2 = int(input("1. Get Employees\n2. Add Employee\n"))
                    match a2:
                        case 1:
                            zoo.get_employees()
                        case 2:
                            a2 = int(
                                input(
                                    "Check profession :\n1. Zoo Keeper\n2. Veterinarian\n"
                                )
                            )
                            match a2:
                                case 1:
                                    name = input("Write name: ")
                                    age = float(input("Write age: "))
                                    zoo_keeper = ZooKeeper(name, age)
                                    zoo.add_employee(zoo_keeper)
                                    print(f"\n{zoo_keeper} -> Добавлен\n")
                                case 2:
                                    name = input("Write name: ")
                                    age = float(input("Write age: "))
                                    veterinarian = Veterinarian(name, age)
                                    zoo.add_employee(veterinarian)
                                    print(f"\n{veterinarian} -> Добавлен\n")
                case 3:
                    print("Exiting Zoo Manager. Goodbye!")
                    break
                case _:
                    print("Please try again!")
    except Exception as e:
        execution_successful = False
        print(f"Произошла ошибка: {e}")
    finally:
        if execution_successful:
            saved_data = zoo.get_info()
            file_manager.save(saved_data)
