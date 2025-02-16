import random


def shuffle_words(text):
    words = text.split()
    random.shuffle(words)
    shuffled_text = " ".join(words)

    return shuffled_text


if __name__ == "__main__":

    text = (
        "Дан текст со словами. Перемешайте все слова этого текста в случайном порядке."
    )
    shuffled_text = shuffle_words(text)
    print(shuffled_text)
