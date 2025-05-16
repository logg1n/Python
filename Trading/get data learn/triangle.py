from enum import Enum
import pandas as pd
from collections import deque
import operator
import logging
from typing import Dict, List

# Если у вас есть модуль для расчёта индикаторов, импортируйте его:
from indicator_manager import IndicatorManager  # замените на актуальное имя вашего модуля

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# -------------------- Класс Triangle (паттерн-детектор) --------------------
class TrendType(Enum):
    BULLISH = 1
    BEARISH = 2

class Triangle:
    def __init__(
        self,
        data: pd.DataFrame,
        trend_type: TrendType = TrendType.BULLISH,
        max_step: int = 4,
        required_peaks: int = 4,
        min_kline: int = 5,
        window_size: int = 8,
    ):
        # DataFrame с предвычисленными признаками (например, SMA_20, EMA_20, и др.)
        self.data = data  
        self.trend_type = trend_type
        self.max_step = max_step
        self.required_peaks = required_peaks
        self.min_kline = min_kline

        # Буферы для накопления экстремумов
        self.peaks: deque = deque(maxlen=window_size)
        self.lows: deque = deque(maxlen=window_size)
        self._buffer: deque = deque(maxlen=4)

        # Счётчики состояния
        self.step_count = 0
        self.peak_count = 0
        self.low_count = 0
        self.kline_count = 0
        self.signal = False

        # Индекс текущей свечи для использования предвычисленных признаков
        self.current_index = 0

    def reset_state(self) -> None:
        """Сброс внутреннего состояния детектора. 
        При этом current_index оставляем неизменным, чтобы поток данных был непрерывным."""
        self.peaks.clear()
        self.lows.clear()
        self._buffer.clear()
        self.step_count = 0
        self.peak_count = 0
        self.low_count = 0
        self.kline_count = 0
        self.signal = False
        logger.debug("Detector state has been reset (pattern detected).")

    def find_pattern(
        self, open: float, high: float, low: float, close: float, volume: float
    ) -> bool:
        """Метод для онлайн‑детекции паттерна.
        Обрабатывает текущую свечу, обновляет внутреннее состояние и,
        если условие выполнено (например, step_count > max_step), сигнализирует о паттерне."""
        self.kline_count += 1
        candle = {
            "open": open,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }

        try:
            self._update_extremes(candle["high"], candle["low"])

            if self._should_reset():
                # Если условие сброса выполнено — паттерн найден, сбросим детектор.
                self.reset_state()
                pattern_found = True
            else:
                pattern_found = self._check_main_conditions(candle)

            self.current_index += 1  # Каждый вызов обновляет индекс (на непрерывном потоке)
            return pattern_found

        except Exception as e:
            logger.error(f"Unexpected error in find_pattern: {str(e)}")
            return False

    def _check_main_conditions(self, candle: dict) -> bool:
        return (
            self._validate_ma_condition()
            and self._check_price_condition(candle["open"], candle["close"])
            and self._check_peaks_condition()
        )

    def _validate_ma_condition(self) -> bool:
        """Проверка условий скользящих средних.
        Если в DataFrame есть предвычисленные признаки, используем их."""
        try:
            if "SMA_20" in self.data.columns and "SMA_50" in self.data.columns:
                sma20 = self.data["SMA_20"].iloc[self.current_index]
                sma50 = self.data["SMA_50"].iloc[self.current_index]
            else:
                sma20 = IndicatorManager.SMA(self.data["close"].tolist(), 20)
                sma50 = IndicatorManager.SMA(self.data["close"].tolist(), 50)

            if "EMA_20" in self.data.columns and "EMA_50" in self.data.columns:
                ema20 = self.data["EMA_20"].iloc[self.current_index]
                ema50 = self.data["EMA_50"].iloc[self.current_index]
            else:
                ema20 = IndicatorManager.EMA(self.data["close"].tolist(), 20)
                ema50 = IndicatorManager.EMA(self.data["close"].tolist(), 50)

            if self.trend_type == TrendType.BULLISH:
                return sma20 > sma50 and ema20 > ema50
            else:
                return sma20 < sma50 and ema20 < ema50

        except Exception as e:
            logger.warning(f"Error in _validate_ma_condition: {str(e)}")
            return False

    def _check_price_condition(self, open_price: float, close: float) -> bool:
        if self.trend_type == TrendType.BULLISH:
            return close > open_price
        else:
            return close < open_price

    def _check_peaks_condition(self) -> bool:
        if self.trend_type == TrendType.BULLISH:
            return self.peak_count >= self.required_peaks
        else:
            return self.low_count >= self.required_peaks

    def _should_reset(self) -> bool:
        """Пример условия: если количество 'шагов' (step_count) превышает max_step,
        считаем, что накопившаяся динамика некорректна и начинаем с чистого листа.
        Это может быть адаптировано под нужную логику паттерна."""
        return self.step_count > self.max_step

    def _update_extremes(self, high: float, low: float) -> None:
        if self.trend_type == TrendType.BULLISH:
            self._process_bullish_extremes(high)
        else:
            self._process_bearish_extremes(low)

    def _process_bullish_extremes(self, high: float) -> None:
        compare_op = operator.gt
        while self.peaks and compare_op(high, self.peaks[-1]):
            self._buffer.append(self.peaks.pop())
            self.peak_count -= 1
        if not self.peaks or compare_op(high, self.peaks[-1]):
            self.peaks.append(high)
            self.peak_count += 1
            self.step_count = 0
        else:
            self.step_count += 1

    def _process_bearish_extremes(self, low: float) -> None:
        compare_op = operator.lt
        while self.lows and compare_op(low, self.lows[-1]):
            self._buffer.append(self.lows.pop())
            self.low_count -= 1
        if not self.lows or compare_op(low, self.lows[-1]):
            self.lows.append(low)
            self.low_count += 1
            self.step_count = 0
        else:
            self.step_count += 1