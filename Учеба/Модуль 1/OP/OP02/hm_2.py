# “Привет [имя]! Тебе [возраст]”


def solve():
    name = input("Введите Ваше имя: ")
    age = input("Введите Ваш возраст: ")

    return f"Привет {name}! Тебе {age}."


if __name__ == "__main__":
    print(solve())
