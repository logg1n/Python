import numpy as np
from collections import deque

from params import Params


class Triangle:

    def __init__(self) -> None:
        self.indicators = ["RSI", "SMA20", "SMA50", "EMA20", "EMA50"]
        self.indicators_values = {
            "RSI": [],
            "EMA20": [],
            "EMA50": [],
            "SMA20": [],
            "SMA50": [],
        }
        self.RSI = self.indicators_values["RSI"]
        self.SMA20 = self.indicators_values["SMA20"]
        self.SMA50 = self.indicators_values["SMA50"]
        self.EMA20 = self.indicators_values["EMA20"]
        self.EMA50 = self.indicators_values["EMA50"]
        self.summary_values = ""

        self.START = []
        self.OPEN = []
        self.HIGH = []
        self.LOW = []
        self.CLOSE = []
        self.last_price = 0.0

        self.peaks = [-float("inf")]
        self.footers = deque(maxlen=4)
        self.to_del = []

        self.SIGNAL = False
        self.Tick = 0
        self.step = 4  # Максимальное количество свечей между вершинами
        self.step_count = 0
        self.peak_count = 1  # Счетчик вершин
        self.kline = 0

    # Вычисляет аномалии, дает сигнал
    def check_crossing(self):
        temp = self.peaks.copy()
        # Вычисление разностей
        diff = np.diff(temp)

        # Поиск мест, где знак разностей меняется
        extrema_indices = np.where(np.diff(np.sign(diff)))[0] + 1

        # Проверка наличия индексов экстремумов
        if not extrema_indices.size:
            if sum(temp) / len(temp) < 1:  #########??????????????
                return True
            elif (
                max(temp) + self.footers[-1]
            ) * Params.Param_OpenPosition <= self.last_price:
                return True
            else:
                return False

        extr = max(temp) - ((max(temp) - self.footers[-1]) * Params.Param_OpenPosition)

        if self.last_price >= extr:
            return True
        return False

    def calculate_difference(self, MA_1, MA_2):
        # Обрезаем списки по наименьшей длине с конца
        min_length = min(len(MA_1), len(MA_2))
        MA_1 = MA_1[-min_length:]
        MA_2 = MA_2[-min_length:]

        # Вычисляем разницу между соответствующими элементами
        differences = [i - j for i, j in zip(MA_1, MA_2)]
        return differences

    def check_dinamic(self, differences):
        val = len(differences) // 4
        s = max(differences[:val])

        trend = True if sum(differences[val:]) / len(differences[val:]) >= s else False
        return trend

    def check_squeeze_prcnt(self):
        min_p = min(self.peaks)
        max_p = max(self.peaks)
        return round(((max_p - min_p) / max_p) * 100, 2)

    def find_triangle(self, open, high, close):
        self.kline += 1

        for p in self.peaks.copy()[::-1]:
            if high >= p:
                self.to_del.insert(0, p)
                self.peak_count -= 1
                if (
                    self.peak_count >= 4
                    and self.kline >= 5
                    and close - open > 0
                    and self.SMA20[-1] > self.SMA50[-1]
                    and self.EMA20[-1] > self.EMA50[-1]
                ):
                    differencesSMA = self.calculate_difference(self.SMA20, self.SMA50)
                    differencesEMA = self.calculate_difference(self.EMA20, self.EMA50)

                    if self.check_dinamic(differencesSMA) and self.check_dinamic(
                        differencesEMA
                    ):
                        self.SIGNAL = True
                        return self.SIGNAL

                if self.peak_count == 0:
                    self.kline = 0
                    self.step_count = 0
                else:
                    self.step_count += 1
                    if self.step_count > self.step:
                        self.peaks.clear()
                        self.peak_count = 0
                        self.kline = 0
                        self.step_count = 0
            else:
                break

        self.peaks = [item for item in self.peaks if item not in self.to_del]
        self.to_del.clear()
        self.peaks.append(high)
        self.footers.append(close)
        self.peak_count += 1
        if self.kline == 0:
            self.kline += 1

        return self.SIGNAL

    def get_tp_or_sl_value(self, lvl, price, side):
        if side == "Buy" and lvl == "tp":
            return round(price + (Params.Param_TakeProfit * price), 4)
        elif side == "Buy" and lvl == "sl":
            return round(price - (Params.Param_StopLoss * price), 4)
        elif side == "Sell" and lvl == "tp":
            return round(price - (Params.Param_TakeProfit * price), 4)
        elif side == "Sell" and lvl == "sl":
            return round(price + (Params.Param_StopLoss * price), 4)
        else:
            return 0
