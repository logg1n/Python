def solve_quadratic(a, b, c):
    d = b**2 - 4 * a * c

    if d > 0:
        x1 = (-b + d**0.5) / (2 * a)
        x2 = (-b - d**0.5) / (2 * a)
        print(f"Корни кватрадного уравнения: {x1}, {x2}")
    elif d == 0:
        x = -b / 2 * a
        print(f"Корни кватрадного уравнения: {x}")
    elif d < 0:
        print(f"Корни кватрадного уравнения: Не имеет корней")


if __name__ == "__main__":
    a = int(input("Введите 1-й коэффициент: "))
    b = int(input("Введите 2-й коэффициент: "))
    c = int(input("Введите 3-й коэффициент: "))

    solve_quadratic(a, b, c)
