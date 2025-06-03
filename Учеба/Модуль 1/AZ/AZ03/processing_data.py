import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


if __name__ == '__main__':
    data = pd.read_csv("divany.csv")
    average_price = int((data["price"].mean()))

    # Создаем гистограмму
    plt.figure(figsize=(14, 6))
    plt.hist(
        data["price"],
        bins = 40,
        color='yellow',
        edgecolor='orange',
        linewidth=1.2,
        alpha=0.7,
        label=f"Средняя цена состовляет: {average_price}"
    )
    plt.xticks(np.arange(0, data["price"].max(), 20000)) # Расширяем диапазон Y

    plt.title("Цены на диваны")
    plt.xlabel("Цена")
    plt.ylabel("Кол-во")
    plt.legend()
    plt.show()