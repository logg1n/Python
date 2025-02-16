import re


def calculate_expression(expression):
    result = eval(expression)

    return result


def solution_str(s):
    pattern = r"([0-9]+|[-+*/**//%])"
    v1, operation, v2 = re.findall(pattern, s)
    val1 = int(v1)
    val2 = int(v2)

    if operation == "-":
        return val1 - val2
    if operation == "+":
        return val1 + val2
    if operation == "*":
        return val1 * val2
    if operation == "/":
        return val1 / val2
    if operation == "**":
        return val1**val2
    if operation == "//":
        return val1 // val2
    if operation == "%":
        return val1 % val2


if __name__ == "__main__":
    str = "10 + 20"
    print(solution_str(str))
