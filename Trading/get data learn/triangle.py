from asyncio.log import logger
from collections import deque
from enum import Enum
import logging
import operator
from typing import Deque

import pandas as pd

from indicator_manager import IndicatorManager

logger = logging.getLogger(__name__)


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
        self.data = data
        self.trend_type = trend_type
        self.max_step = max_step
        self.required_peaks = required_peaks
        self.min_kline = min_kline

        # Инициализация структур данных
        self.peaks: Deque[float] = deque(maxlen=window_size)
        self.lows: Deque[float] = deque(maxlen=window_size)
        self._buffer: Deque[float] = deque(maxlen=4)

        # Счетчики состояния
        self.step_count = 0
        self.peak_count = 0
        self.low_count = 0
        self.kline_count = 0
        self.signal = False

    def reset_state(self) -> None:
        """Полный сброс состояния детектора"""
        self.peaks.clear()
        self.lows.clear()
        self._buffer.clear()
        self.step_count = 0
        self.peak_count = 0
        self.low_count = 0
        self.kline_count = 0
        self.signal = False

    def find_pattern(
        self, open: float, high: float, low: float, close: float, volume: float
    ) -> bool:
        """Основной метод обнаружения паттерна"""
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
                logger.debug("Resetting detector state")
                self.reset_state()
                return False

            return self._check_main_conditions(candle)

        except KeyError as e:
            logger.error(f"Key error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False

    def _check_main_conditions(self, candle: dict) -> bool:
        """Проверка основных условий паттерна"""

        return all(
            [
                self._validate_ma_condition(),
                self._check_price_condition(candle["open"], candle["close"]),
                self._check_peaks_condition(),
            ]
        )

    def _validate_ma_condition(self) -> bool:
        """Проверка условий скользящих средних"""
        try:
            sma20: float = IndicatorManager.SMA(self.data["close"].to_list(), 20)
            sma50: float = IndicatorManager.SMA(self.data["close"].to_list(), 50)
            ema20: float = IndicatorManager.EMA(self.data["close"].to_list(), 20)
            ema50: float = IndicatorManager.EMA(self.data["close"].to_list(), 50)

            if self.trend_type == TrendType.BULLISH:
                return sma20 > sma50 and ema20 > ema50
            return sma20 < sma50 and ema20 < ema50

        except (IndexError, KeyError) as e:
            logger.warning(f"MA values not available: {str(e)}")
            return False

    def _check_price_condition(self, open_price: float, close: float) -> bool:
        """Проверка направления цены"""
        return (
            close > open_price
            if self.trend_type == TrendType.BULLISH
            else close < open_price
        )

    def _check_peaks_condition(self) -> bool:
        """Проверка количества экстремумов"""
        if self.trend_type == TrendType.BULLISH:
            return self.peak_count >= self.required_peaks
        return self.low_count >= self.required_peaks

    def _should_reset(self) -> bool:
        """Определение необходимости сброса состояния"""
        reset_conditions = [
            self.step_count > self.max_step,
            self.trend_type == TrendType.BULLISH and self.peak_count < 1,
            self.trend_type == TrendType.BEARISH and self.low_count < 1,
        ]
        return any(reset_conditions)

    def _update_extremes(self, high: float, low: float) -> None:
        """Обновление экстремумов в зависимости от тренда"""
        if self.trend_type == TrendType.BULLISH:
            self._process_bullish_extremes(high)
        else:
            self._process_bearish_extremes(low)

    def _process_bullish_extremes(self, high: float) -> None:
        """Обработка экстремумов для бычьего тренда"""
        compare_op = operator.gt
        current_extremes = self.peaks

        while current_extremes and compare_op(high, current_extremes[-1]):
            self._buffer.append(current_extremes.pop())
            self.peak_count -= 1

        if not current_extremes or compare_op(high, current_extremes[-1]):
            current_extremes.append(high)
            self.peak_count += 1
            self.step_count = 0
        else:
            self.step_count += 1

    def _process_bearish_extremes(self, low: float) -> None:
        """Обработка экстремумов для медвежьего тренда"""
        compare_op = operator.lt
        current_extremes = self.lows

        while current_extremes and compare_op(low, current_extremes[-1]):
            self._buffer.append(current_extremes.pop())
            self.low_count -= 1

        if not current_extremes or compare_op(low, current_extremes[-1]):
            current_extremes.append(low)
            self.low_count += 1
            self.step_count = 0
        else:
            self.step_count += 1

    def __repr__(self) -> str:
        return (
            f"TrianglePatternDetector("
            f"trend={self.trend_type.name}, "
            f"peaks={self.peak_count}, "
            f"steps={self.step_count})"
        )
