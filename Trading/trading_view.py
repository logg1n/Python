from tradingview_ta import TA_Handler, Interval


class Trading_View:
    @staticmethod
    def set_indicator_values(symbol, interval, indicators):
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

        handler = TA_Handler(
            symbol=f"{symbol}.P",
            screener="crypto",
            exchange="BYBIT",
            interval=t_i.get(interval),  # type: ignore
        )

        analysis = handler.get_analysis()
        return {indicator: analysis.indicators[indicator] for indicator in indicators}

    @staticmethod
    def checkSymbols(tickers):
        """
        Args:
            tickers (list or dict): Список или словарь тикеров.

        Returns:
            ist: Список тикеров.
        """

        tk = []
        for sym in tickers:
            handler = TA_Handler(
                symbol=sym,
                screener="crypto",
                exchange="BYBIT",
                interval=Interval.INTERVAL_15_MINUTES,
            )
            try:
                handler.get_indicators(["RSI"])
                tk.append(sym)
            except Exception:
                continue
        return tk

    @staticmethod
    def checkSymbol(symbol):
        """
        Args:
            symbol (str): Тикер.

        Returns:
            bool: True, если индикатор "RSI" получен, иначе False.
        """

        handler = TA_Handler(
            symbol=symbol,
            screener="crypto",
            exchange="BYBIT",
            interval=Interval.INTERVAL_15_MINUTES,
        )
        try:
            handler.get_indicators(["RSI"])
            return True
        except Exception:
            return False
