import re


# ------------------------------
def alternative(s: str):
    return all(char.isdigit() and int(char) % 2 == 0 for char in s)


# ------------------------------


def split_text(text):
    delimiters = r"[,\s;.!?]+"

    return re.split(delimiters, text)


def get_even_num_in_str(lt):
    if all(num.isdigit() for num in lt):
        filtered_result = [int(num) for num in lt]
        return all(num % 2 == 0 for num in filtered_result)
    else:
        return False


if __name__ == "__main__":
    print(get_even_num_in_str(split_text("2 2 2")))
    print(get_even_num_in_str(split_text("2 a 2")))
    print(get_even_num_in_str(split_text("222")))

    print(alternative("2 2 2"))
    print(alternative("222"))
