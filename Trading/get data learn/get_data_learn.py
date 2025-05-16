import argparse
import time
import pandas as pd
import os
from typing import List, Dict
from datetime import datetime
from bybit_client import BybitTradingClient
from cursor import Cursor


def parse_arguments():
   parser = argparse.ArgumentParser(
      description="Скрипт для получения исторических данных с Bybit"
   )
   parser.add_argument('--timeframe', type=str, required=True,
                       help='Таймфрейм (например "60" или "15 60 240")')
   parser.add_argument('--tradingpair', type=str, required=True,
                       help='Торговые пары через пробел (например "BTCUSDT ETHUSDT")')
   parser.add_argument('--date', type=str, required=True,
                       help='Дата начала в формате DD.MM.YYYY')
   parser.add_argument('--limit', type=int, default=1000,
                       help='Лимит свечей на запрос (по умолчанию 1000)')
   parser.add_argument('--iteration', type=int, default=10,
                       help='Количество итераций (по умолчанию 10)')
   return parser.parse_args()


def fetch_data(client: BybitTradingClient, cursor: Cursor, pair: str, tf: str):
   for _ in range(args.iteration):
      try:
         data = client.get_historical_data(
            symbol=pair,
            timeframe=tf,
            start=cursor.curs,
         )

         if data is None or data.empty:
            print(f"Нет данных для {pair} {tf}")
            break

         yield data
         cursor.next_cursor()
         time.sleep(1)  # Задержка для API

      except Exception as e:
         print(f"Ошибка для {pair} {tf}: {str(e)}")
         break


def save_to_file(data: pd.DataFrame, pair: str, tf: str):
   filename = f"data/{pair}_{tf}.csv"
   os.makedirs("data", exist_ok=True)

   # Если файл существует, дописываем данные
   if os.path.exists(filename):
      data.to_csv(filename, mode='a', header=False, index=False)
   else:
      data.to_csv(filename, index=False)
   print(f"Сохранено {len(data)} строк в {filename}")


def main():
   global args
   args = parse_arguments()

   client = BybitTradingClient()
   pairs = args.tradingpair.split()
   timeframes = args.timeframe.split()

   for pair in pairs:
      for tf in timeframes:
         print(f"\nОбработка {pair} {tf}...")
         cursor = Cursor(tf, args.date)

         for chunk in fetch_data(client, cursor, pair, tf):
            save_to_file(chunk, pair, tf)


if __name__ == "__main__":
   main()