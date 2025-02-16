val1 = float(input("Ведите 1-е число: "))
val2 = float(input("Ведите 2-е число: "))
print()
operation = input("Выберите операцию  + - * /\n")

match operation:
    case "+":
        print(val1 + val2)
    case "-":
        print(val1 - val2)
    case "*":
        print(val1 * val2)
    case "/":
        print(val1 / val2)
