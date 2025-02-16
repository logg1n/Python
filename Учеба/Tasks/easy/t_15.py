def get_prelast_ch(str):
    if len(str) > 1:
        return str[-2]
    else:
        return ""


if __name__ == "__main__":
    print(get_prelast_ch("dsfds sefrds"))
    print(get_prelast_ch("d"))
