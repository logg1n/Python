import pandas as pd
import numpy as np


class IndicatorManager:
   @staticmethod
   def SMA(prices: list, window: int) -> float:
      """
        Возвращает последнее значение скользящей средней (Simple Moving Average, SMA)
        для списка цен, рассчитанное по окну заданного размера.
        """
      if len(prices) < 1:
         return np.nan
      # Используем min_periods=1, чтобы для первых значений окна использовать имеющиеся данные
      return pd.Series(prices).rolling(window=window, min_periods=1).mean().iloc[-1]

   @staticmethod
   def SMA_series(prices: list, window: int) -> pd.Series:
      """
        Возвращает серию значений скользящей средней (SMA) для списка цен.
        Для каждой позиции рассчитывается среднее по предыдущим 'window' значениям.
        """
      if len(prices) < 1:
         return pd.Series([])
      return pd.Series(prices).rolling(window=window, min_periods=1).mean()

   @staticmethod
   def EMA(prices: list, window: int) -> float:
      """
        Возвращает последнее значение экспоненциальной скользящей средней (EMA)
        для списка цен.
        """
      if len(prices) < 1:
         return np.nan
      return pd.Series(prices).ewm(span=window, adjust=False).mean().iloc[-1]

   @staticmethod
   def EMA_series(prices: list, window: int) -> pd.Series:
      """
        Возвращает серию значений EMA для списка цен.
        """
      if len(prices) < 1:
         return pd.Series([])
      return pd.Series(prices).ewm(span=window, adjust=False).mean()

   @staticmethod
   def RSI(prices: list, window: int = 14) -> float:
      """
        Возвращает последнее значение индекса относительной силы (RSI)
        для списка цен.
        При недостатке данных возвращается нейтральное значение 50.0.
        """
      if len(prices) < 2:
         return 50.0

      series = pd.Series(prices)
      delta = series.diff()
      gain = delta.where(delta > 0, 0.0)
      loss = -delta.where(delta < 0, 0.0)

      # Рассчитываем скользящие средние для прироста и убытка
      avg_gain = gain.rolling(window=window, min_periods=1).mean()
      avg_loss = loss.rolling(window=window, min_periods=1).mean()

      last_avg_gain = avg_gain.iloc[-1]
      last_avg_loss = avg_loss.iloc[-1]

      if last_avg_loss == 0:
         return 100.0 if last_avg_gain != 0 else 50.0

      rs = last_avg_gain / last_avg_loss
      return 100 - (100 / (1 + rs))

   @staticmethod
   def RSI_series(prices: list, window: int = 14) -> pd.Series:
      """
        Возвращает серию значений RSI для списка цен.
        Для каждого элемента рассчитывается RSI с использованием скользящего окна.
        """
      series = pd.Series(prices)
      delta = series.diff()
      gain = delta.where(delta > 0, 0.0)
      loss = -delta.where(delta < 0, 0.0)

      avg_gain = gain.rolling(window=window, min_periods=1).mean()
      avg_loss = loss.rolling(window=window, min_periods=1).mean()

      # Предотвращаем деление на ноль, заменяя нулевые значения на небольшое число или
      # применяя специальную логику.
      rs = avg_gain / avg_loss.replace(0, np.nan).ffill().fillna(1)
      rsi = 100 - (100 / (1 + rs))
      # Если убытков никаких (avg_loss == 0), то устанавливаем RSI по правилу:
      # если есть приросты, то 100, если нет, то 50.
      rsi[avg_loss == 0] = np.where(avg_gain[avg_loss == 0] != 0, 100.0, 50.0)
      return rsi

   @staticmethod
   def VOLATILITY(df: pd.DataFrame,
                  period: int = 100,
                  price_col: str = "close",
                  annualized: bool = True,
                  min_volatility: float = None) -> pd.Series:
      """
        Рассчитывает историческую волатильность на основе логарифмических доходностей.
        Возвращает серию значений волатильности (в процентах).

        Параметры:
          - df: DataFrame с данными.
          - period: длина окна для расчета волатильности.
          - price_col: Название колонки с ценами.
          - annualized: Если True — шкалирование до годового значения.
          - min_volatility: Минимальный порог волатильности; если значение ниже порога, то заменяется на NaN.
        """
      if price_col not in df.columns:
         raise ValueError(f"Колонка {price_col} не найдена в DataFrame")

      # Вычисляем логарифмические доходности
      log_returns = np.log(df[price_col] / df[price_col].shift(1))
      # Рассчет стандартного отклонения доходности по указанному периоду
      volatility = log_returns.rolling(window=period, min_periods=1).std()

      if annualized:
         # Пример масштабирования до годового значения для дневных данных (252 торговых дня)
         volatility *= np.sqrt(252)

      volatility = volatility * 100  # Переводим в проценты

      if min_volatility is not None:
         if not isinstance(min_volatility, (int, float)) or min_volatility < 0:
            raise ValueError("min_volatility должен быть положительным числом")
         volatility = volatility.where(volatility >= min_volatility, np.nan)
      return volatility

   @staticmethod
   def VOLATILITY_value(df: pd.DataFrame,
                        period: int = 100,
                        price_col: str = "close",
                        annualized: bool = True,
                        min_volatility: float = None) -> float:
      """
        Возвращает последнее значение волатильности (в процентах) для DataFrame.
        """
      vol_series = IndicatorManager.VOLATILITY(df, period, price_col, annualized, min_volatility)
      return vol_series.iloc[-1]
