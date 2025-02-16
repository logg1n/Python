import math


def square(a):
    return (
        round(a * 4, 2),
        round(a**2, 2),
        round(a * math.sqrt(2), 2),
    )


if __name__ == "__main__":
    val = float(input("Введите сторону квадрата: "))
    print(square(val))
