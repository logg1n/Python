def conv(sec):
    min = sec // 60
    hours = min // 60
    days = hours // 24

    return f"{days}:{hours:02}:{min:02}:{sec:02}"


if __name__ == "__main__":
    print(conv(sec=86400))
