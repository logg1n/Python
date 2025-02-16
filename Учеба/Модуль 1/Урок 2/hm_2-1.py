from datetime import datetime


def calculate_life_duration(age):
    now = datetime.now()

    years = age
    months = years * 12
    days = years * 365 + (years // 4)  # Учитываем високосные годы
    hours = days * 24

    return {"years": years, "months": months, "days": days, "hours": hours}


def solve():
    name = input("Введите Ваше имя: ")
    while True:
        try:
            age = int(input("Введите Ваш возраст: "))
            break
        except ValueError:
            print("Пожалуйста, введите корректное число для возраста.")

    duration = calculate_life_duration(age)

    print()
    print(f"Привет, {name}! Тебе {duration['years']} лет.")
    print(f"Это эквивалентно {duration['months']} месяцам.")
    print(f"Это эквивалентно {duration['days']} дням.")
    print(f"Это эквивалентно {duration['hours']} часам.")


if __name__ == "__main__":
    solve()
