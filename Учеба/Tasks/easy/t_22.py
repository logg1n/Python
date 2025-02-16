# [1, 12, 5, 23, 7, 34, 9, 45, 3, 56


def past_num(nums: list):
    lt = nums[:]

    for indx, n in enumerate(nums):
        if n > -10 and n < 10:
            lt.insert(indx + 1, n)

    return lt


if __name__ == "__main__":
    print(past_num(nums=[1, 12, 1, 23, 7, 34, 9, 45, 3, 56]))
