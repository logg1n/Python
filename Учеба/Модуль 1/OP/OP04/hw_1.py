val1 = int(input("Введите первое число: "))
val2 = int(input("Введите второе число: "))
val3 = int(input("Введите третье число: "))


if val1 < val2 and val1 < val3:
    print(f"Наименьшее число: {val1}")
elif val2 < val1 and val2 < val3:
    print(f"Наименьшее число: {val2}")
else:
    print(f"Наименьшее число: {val3}")
