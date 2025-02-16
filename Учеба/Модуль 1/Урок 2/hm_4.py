def rectangle_area():

    length = float(input("Введите длину прямоугольника: "))
    width = float(input("Введите ширину прямоугольника: "))

    return length * width


if __name__ == "__main__":
    print(f"Площадь прямоугольника: {rectangle_area()}")
