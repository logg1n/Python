import getpass
import random

game = {1: "Камень", 2: "Ножницы", 3: "Бумага"}


def check_winner(v1, v2):
    v1 = int(v1)
    v2 = int(v2)

    print("------------------------------------------")
    match v1 * v2:
        case 1:
            print("Ничья")
        case 2:
            if v1 == 1:
                print("Победил игрок 1")
            else:
                print("Проиграл игрок 1")
        case 3:
            print("Проиграл игрок 1")
        case 4:
            print("Ничья")
        case 6:
            if v1 == 2:
                print("Победил игрок 1")
            else:
                print("Проиграл игрок 1")
        case 9:
            print("Ничья")
    print("------------------------------------------")


while True:

    val = int(input("Выберите вариант:\n\t1. 1 vs CPU\n\t2. 1 vs 1\n\t3. Выход\n  "))
    match val:
        case 1:
            print("Варианты: \n1. Камень\n2. Ножницы\n3. Бумага")
            val1 = int(input("Ход 1-го игрока: "))
            print("Ходит CPU")
            val2 = random.choice(list(game.keys()))

            check_winner(val1, val2)
        case 2:
            print("Варианты: \n1. Камень\n2. Ножницы\n3. Бумага")
            val1 = int(getpass.getpass("Ход 1-го игрока: "))
            val2 = int(getpass.getpass("Ход 2-го игрока: "))

            check_winner(val1, val2)
        case 3:
            break
