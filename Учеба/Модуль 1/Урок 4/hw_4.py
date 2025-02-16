val1 = int(input("Введите начало диапазона: "))
val2 = int(input("Введите окончание диапазона: "))

for i in range(val1, val2 + 1):
    if i % 2 == 0:
        print(i)
