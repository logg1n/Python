import argparse
import time

import pandas as pd

from bybit_client import BybitTradingClient

from cursor import Cursor

if __name__ == "__main__":
    # Парсим аргументы командной строки
    parser = argparse.ArgumentParser(description="Скрипт для получения исторических данных по криптовалютам.")
    parser.add_argument('--timeframe', type=str, required=True, help='Интервал времени (например, "60" для 60 минут)')
    parser.add_argument('--limit', type=int, required=True, help='Количество свечей на запрос (например, 100)')
    parser.add_argument('--date', type=str, required=True, help='Начальная дата в формате "%d.%m.%Y" (например, "01.01.2020")')
    parser.add_argument('--iteration', type=int, required=True, help='Количество итераций для получения данных')
    args = parser.parse_args()

    candle_data: pd.DataFrame = pd.DataFrame()
    timeframe: str = args.timeframe
    limit: int = args.limit
    date: str = args.date
    iteration: int = args.iteration
    symbol: str = "BTCUSD"


    # Инициализируем клиента и курсор
    client: BybitTradingClient = BybitTradingClient(timeframe, limit)
    cursor: Cursor = Cursor(client.timeframe, client.limit, date)

    for _ in range(iteration):
        # Получаем исторические данные
        start_time_ms = cursor.curs
        historical_data: pd.DataFrame = client.get_historical_data(symbol, start_time_ms)
        # Проверяем, что данные получены
        if historical_data is None or historical_data.empty:
            print("Нет данных для загрузки или произошла ошибка при получении данных.")

            break
        # Добавляем данные к общему DataFrame
        candle_data = pd.concat([candle_data, historical_data], ignore_index=True)
        # Обновляем курсор
        cursor.next_cursor()
        # Задержка между запросами
        time.sleep(2)

    # Сохраняем данные в CSV файл
    # Формируем имя файла в формате date_timeframe_колво строк в dataframe.csv
    formatted_date = date.replace('.', '-')
    filename = f"{formatted_date}_{timeframe}_{len(candle_data)}.csv"

    candle_data.to_csv(filename, index=False)
    print(f"Данные успешно сохранены в файл {filename}")
    print(f"Загружено данных {len(candle_data)}")
