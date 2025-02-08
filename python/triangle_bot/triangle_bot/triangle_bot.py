import sys

sys.path.insert(0, "C:\\Users\\loggi\\github\\python\\trade\\trade")
import order as tt
import order_book as ob
import connect_wallet as cw

import logging
import traceback
import sys
import numpy as np

from pybit.unified_trading import HTTP
from pybit.unified_trading import WebSocket
from tradingview_ta import TA_Handler, Interval
from time import sleep, strftime, localtime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{sys.argv[1]}.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)

# Создание и настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

connector = cw.Connector()
OrderBook = ob.OrderBook()

# Инициализация списков
indicators = ["RSI", "SMA20", "SMA50", "EMA20", "EMA50"]
indicators_values = {"RSI": [], "EMA20": [], "EMA50": [], "SMA20": [], "SMA50": []}
RSI = indicators_values["RSI"]
SMA20 = indicators_values["SMA20"]
SMA50 = indicators_values["SMA50"]
EMA20 = indicators_values["EMA20"]
EMA50 = indicators_values["EMA50"]
summary_values = ""

START = []
OPEN = []
HIGH = []
LOW = []
CLOSE = []

atr = []
peaks = [-float("inf")]
to_del = []

Tick = 0
step = 4  # Максимальное количество свечей между вершинами\
step_count = 0
peak_count = 1  # Счетчик вершин
kline = 0


# Функция для проверки сигнала if j != -1 нужно вычиcлять atr[len(arr) -1 - j]
def check_crossing():
    try:
        t_atr = atr.copy()

        # Вычисление разностей
        diff = np.diff(t_atr)
        # Поиск мест, где знак разностей меняется
        extrema_indices = np.where(np.diff(np.sign(diff)))[0] + 1
        # Экстремумы
        extrema = [t_atr[i] for i in extrema_indices]

        v = (extrema[0] - max(extrema[1:-2])) / 2
        j = -1
        i = next((l for l, k in enumerate(t_atr) if k == extrema[-1]), -1)
        if i != -1:
            t_atr = t_atr[i:]
            j = next(
                (l + 1 for l, k in enumerate(t_atr[::-1]) if k >= extrema[0] - v), -1
            )
            if j != -1:
                return True

        return False
    except Exception as err:
        logging.error(f"Произошла ошибка: {str(err)}")
        traceback.print_exc(file=sys.stderr)


def set_indicator_values(symbol, interval):
    global indicators_values
    global summary_values

    t_i = {
        "1": Interval.INTERVAL_1_MINUTE,
        "5": Interval.INTERVAL_5_MINUTES,
        "15": Interval.INTERVAL_15_MINUTES,
        "30": Interval.INTERVAL_30_MINUTES,
        "60": Interval.INTERVAL_1_HOUR,
        "120": Interval.INTERVAL_2_HOURS,
        "240": Interval.INTERVAL_4_HOURS,
        "D": Interval.INTERVAL_1_DAY,
        "W": Interval.INTERVAL_1_WEEK,
        "M": Interval.INTERVAL_1_MONTH,
    }

    try:
        handler = TA_Handler(
            symbol=f"{symbol}.P",
            screener="crypto",
            exchange="BYBIT",
            interval=t_i.get(interval),  # type: ignore
        )
        analysis = handler.get_analysis()
        # Добавление значений индикаторов в соответствующие списки
        for indicator in indicators:
            indicators_values[indicator].append(analysis.indicators[indicator])  # type: ignore
        # Добавление сводки анализа в список
        summary_values = analysis.summary["RECOMMENDATION"]  # type: ignore

    except Exception as err:
        logging.error(f"Произошла ошибка: {str(err)}")
        traceback.print_exc(file=sys.stderr)


def calculate_difference(list1, list2):
    if len(list1) != len(list2):
        return "Списки разной длины!"
    differences = [i - j for i, j in zip(list1, list2)]
    return differences


def check_dinamic(differences):
    val = len(differences) // 4
    s = max(differences[:val])
    print(s, val)

    trend = True if sum(differences[val:]) / len(differences[val:]) >= s else False
    return trend


def milliseconds_to_date(u_time):
    try:
        return strftime("%a, %d %b %Y %H:%M ", localtime(u_time / 1000))
    except Exception as err:
        logging.error(f"Произошла ошибка: {str(err)}")
        traceback.print_exc(file=sys.stderr)


def find_triangle(open, high, close):
    global step
    global step_count
    global peak_count
    global peaks
    global kline

    try:
        connector.send(0)
        atr_one = abs(open - close)

        kline += 1
        atr.append(atr_one)
        for p in peaks.copy()[::-1]:
            balance = connector.receive()
            if high >= p:
                to_del.insert(0, p)
                peak_count -= 1
                if (
                    peak_count >= 4
                    and kline >= 5
                    and close - open > 0
                    and SMA20[-1] > SMA50[-1]
                    and EMA20[-1] > EMA50[-1]
                ):
                    differencesSMA = calculate_difference(SMA20, SMA50)
                    differencesEMA = calculate_difference(EMA20, EMA50)

                    if (
                        check_dinamic(differencesSMA)
                        and check_dinamic(differencesEMA)
                        and check_crossing()
                    ):
                        order = tt.Order(
                            get_lastPrice(),
                            max(peaks)
                            + (
                                (max(peaks) - min(peaks))
                                - ((max(peaks) - min(peaks)) * (0.75 / 100))
                            ),
                            min(peaks[-4:]) - (min(peaks[-4:]) - balance * (0.5 / 100)),
                            balance,
                        )
                        OrderBook.append(order)
                        logging.info(order.str(sys.argv[1], high))
                        traceback.print_exc(file=sys.stderr)

                if peak_count == 0:
                    kline = 0
                    step_count = 0
                else:
                    step_count += 1
                    if step_count > step:
                        peaks.clear()
                        peak_count = 0
                        kline = 0
                        step_count = 0
            else:
                break

        peaks = [item for item in peaks if item not in to_del]
        to_del.clear()
        peaks.append(high)
        peak_count += 1
        if kline == 0:
            kline += 1

    except Exception as err:
        logging.error(f"Произошла ошибка: {str(err)}")
        traceback.print_exc(file=sys.stderr)


def get_lastPrice():
    session = HTTP(testnet=True)

    return float(
        session.get_tickers(
            category="linear",
            symbol="BTCUSD",
        )[
            "result"
        ][  # type: ignore
            "list"
        ][
            0
        ][
            "lastPrice"
        ]
    )


def handle_kline(m):
    global Tick
    global START
    global OPEN
    global HIGH
    global LOW
    global CLOSE

    try:
        d = m.get("data", {})
        t = m.get("topic").split(".")[1:]

        high = float(d[0]["high"])
        low = float(d[0]["low"])

        for order in OrderBook.get_book():
            if order.fulfill == tt.Status.OPEN:
                if low <= order.sl:
                    order.set(low, tt.Status.STOP_LOSS)
                    logging.info(order.str({sys.argv[1], sys.argv[2]}, high))
                    traceback.print_exc(file=sys.stderr)
                if high >= order.tp:
                    order.set(high, tt.Status.TAKE_PROFIT)
                    logging.info(order.str({sys.argv[1], sys.argv[2]}, high))
                    traceback.print_exc(file=sys.stderr)
        if d[0]["confirm"]:
            Tick += 1
            START.append(float(d[0]["start"]))
            OPEN.append(float(d[0]["open"]))
            HIGH.append(float(d[0]["high"]))
            LOW.append(float(d[0]["low"]))
            CLOSE.append(float(d[0]["close"]))

            set_indicator_values(t[-1], t[0])
            find_triangle(OPEN[-1], HIGH[-1], CLOSE[-1])
        if Tick >= 192:
            START = START[97:]
            OPEN = OPEN[97:]
            HIGH = HIGH[97:]
            LOW = LOW[97:]
            CLOSE = CLOSE[97:]
    except Exception as err:
        logging.error(f"Произошла ошибка: {str(err)}")
        traceback.print_exc(file=sys.stderr)


def connect(ticker, interval):
    try:
        ws = WebSocket(testnet=True, channel_type="linear")
        ws.kline_stream(interval=int(interval), symbol=ticker, callback=handle_kline)

        logging.info(f"{ticker} - connected")
        traceback.print_exc(file=sys.stderr)

        print(f"{ticker} - connected")

        while True:

            sleep(1)
    except Exception as err:
        logging.error(f"Произошла ошибка: {str(err)}")
        traceback.print_exc(file=sys.stderr)


# 1 5 15 30 (min)
# 60 120 240 (min)
# D (day)
# W (week)
# M (month)
if __name__ == "__main__":
    try:
        connect(sys.argv[1], sys.argv[2])
    except Exception as err:
        logging.error(f"Произошла ошибка: {str(err)}")
        traceback.print_exc(file=sys.stderr)
