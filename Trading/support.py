import locale
import json
import logging
import os
from time import localtime, strftime
from tradingview_ta import TA_Handler, Interval


class Support:
    @staticmethod
    def set_logger(folder, file) -> logging.Logger:
        dir_path = os.path.dirname(os.path.realpath(__file__))

        if not os.path.exists(os.path.join(dir_path, folder)):
            os.makedirs(os.path.join(dir_path, folder))
        if not os.path.isfile(os.path.join(dir_path, folder, f"{file}.log")):
            open(os.path.join(dir_path, folder, f"{file}.log"), "w").close()

        logging.basicConfig(
            level=logging.INFO,
            filename=os.path.join(dir_path, folder, f"{file}.log"),
            filemode="w",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        return logger

    @staticmethod
    def set_locale():
        locale.setlocale(locale.LC_ALL, "Russian_Russia.1251")

    @staticmethod
    def reset_locale():
        locale.setlocale(locale.LC_ALL, "")

    @staticmethod
    def milliseconds_to_date(u_time):
        return strftime("%a, %d %b %Y %H:%M ", localtime(u_time / 1000))

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
    def checkSymbol(tickers):
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
    def build_order(
        ticker,
        side,
        price: float,
        tp: float,
        sl: float,
        risk_limit: float,
        balance: float,
        minQty: float,
        maxQty: float,
        order_link_id,
    ):
        coff_position = 0.45 / 100

        qty_usdt = (balance * coff_position) * risk_limit
        qty_ticker = qty_usdt / price

        qty_ticker = min(max(qty_ticker, minQty), maxQty)
        if qty_ticker > 0:
            qty_ticker = round(qty_ticker, 0)
        else:
            qty_ticker = round(qty_ticker, 4)

        t = json.dumps(
            {
                "category": "linear",
                "symbol": ticker,
                "side": side,
                "orderType": "Market",
                "qty": str(qty_ticker),
                "triggerBy": "LastPrice",
                "timeInForce": "GTC",
                "positionIdx": 0,
                "takeProfit": str(tp),
                "stopLoss": str(sl),
                "tpTriggerBy": "MarkPrice",
                "slTriggerBy": "IndexPrice",
                "orderLinkId": order_link_id,
                "isLeverage": 1,
            }
        )

        return t
