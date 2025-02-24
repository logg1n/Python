import pandas as pd
import numpy as np


class IndicatorManager:
    def SMA(prices: list, window: int) -> float:
        """Возвращает последнее значение SMA для списка цен"""
        if len(prices) < 1:
            return np.nan
        return pd.Series(prices).rolling(min_periods=1, window=window).mean().iloc[-1]

    def EMA(prices: list, window: int) -> float:
        """Возвращает последнее значение EMA для списка цен"""
        if len(prices) < 1:
            return np.nan
        return pd.Series(prices).ewm(span=window, adjust=False).mean().iloc[-1]

    def RSI(prices: list, window: int = 14) -> float:
        """Возвращает последнее значение RSI для списка цен"""
        if len(prices) < 2:
            return 50.0  # Нейтральное значение при недостатке данных

        series = pd.Series(prices)
        delta = series.diff()

        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        avg_gain = gain.rolling(window).mean().iloc[-1]
        avg_loss = loss.rolling(window).mean().iloc[-1]

        if avg_loss == 0:
            return 100.0 if avg_gain != 0 else 50.0

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def VOLATILITY(
        df: pd.DataFrame,
        period: int = 100,
        price_col: str = "close",
        annualized: bool = True,
        min_volatility: float = None,
    ) -> pd.Series:
        """
        Расчет исторической волатильности с проверкой минимального уровня

        Параметры:
        df - DataFrame с данными
        period - период расчета в барах (по умолчанию 100)
        price_col - название колонки с ценами (по умолчанию 'close')
        annualized - годовое масштабирование (по умолчанию True)
        min_volatility - минимальный порог волатильности (в %). Если None - проверка отключена

        Возвращает:
        Series с значениями волатильности (в %), где значения ниже min_volatility заменены на NaN
        """
        if price_col not in df.columns:
            raise ValueError(f"Колонка {price_col} не найдена в DataFrame")

        # Рассчитываем логарифмические доходности
        log_returns: pd.Series = np.log(df[price_col] / df[price_col].shift(1))

        # Вычисляем стандартное отклонение за период
        volatility = log_returns.rolling(window=period).std()

        if annualized:
            # Масштабируем до годового значения
            # volatility *= np.sqrt(252)

            # Часовые данные:
            volatility *= np.sqrt(252 * 24)

        # 15-минутные:
        # volatility *=np.sqrt(252*24*4)

        # Конвертируем в проценты
        volatility = volatility.round(4) * 100

        # Проверка минимальной волатильности
        if min_volatility is not None:
            if not isinstance(min_volatility, (int, float)) or min_volatility < 0:
                raise ValueError("min_volatility должен быть положительным числом")
            volatility = volatility.where(volatility >= min_volatility, np.nan)

        return volatility
