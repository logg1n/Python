from functools import partial
from multiprocessing import Process
import json
import os
from dotenv import load_dotenv
import sys

from time import localtime, sleep, strftime
import traceback
import websocket
from pybit.unified_trading import HTTP


from web_socket import WebSocketClient
from logger import Support
from trading_view import Trading_View
from strategy.triangle import Triangle
from params import Params

load_dotenv()

API_KEY = os.getenv("DEMO_API_KEY")
SECRET_KEY = os.getenv("DEMO_SECRET_KEY")

session = HTTP(
    api_key=API_KEY,
    api_secret=SECRET_KEY,
)
# Переопределение базового URL для демо-сервера
session.endpoint = "https://api-demo.bybit.com"

Subs = [
    "tickers",
    "kline",
]

Log = Support.set_logger()


def handle_kline(ticker_info: dict, strategy: Triangle, ws, msg):
    try:
        msg_json = json.loads(msg)
        msg_dict = dict(msg_json)

        if msg_dict.get("op"):
            print(f"INFO -> {msg}")
            Log.info(f"INFO -> {msg}")
        elif str(msg_dict.get("topic")).split(".")[0] == Subs[1]:
            ticker = str(msg_dict.get("topic")).split(".")[-1]
            data_K = msg_dict.get("data", {})[0]
            strategy.last_price = float(data_K["open"])
            if data_K["confirm"]:
                strategy.START.append(float(data_K["start"]))
                strategy.OPEN.append(float(data_K["open"]))
                strategy.HIGH.append(float(data_K["high"]))
                strategy.LOW.append(float(data_K["low"]))
                strategy.CLOSE.append(float(data_K["close"]))
                temp = Trading_View.set_indicator_values(
                    ticker, str(Params.Param_Interval), strategy.indicators
                )
                for key in strategy.indicators_values:
                    if key in temp:
                        # Добавляем новые значения из temp в соответствующий список в indicators_values
                        strategy.indicators_values[key].append(temp[key])
                if (
                    strategy.find_triangle(
                        strategy.OPEN[-1], strategy.HIGH[-1], strategy.CLOSE[-1]
                    )
                    and strategy.check_squeeze_prcnt() < Params.Param_Squeeze
                ):
                    if strategy.check_crossing():
                        #
                        try:
                            wallet_balance = 0.0
                            response: dict = session.get_wallet_balance(
                                accountType="UNIFIED",
                                coin="USDT",
                            )
                            result: dict = response.get("result")
                            coin: dict = result.get("list")[0]
                            balance: dict = coin.get("coin")[0]
                            try:
                                wallet_balance = float(balance.get("walletBalance"))
                            except (TypeError, ValueError):
                                wallet_balance = 0.0
                                print(
                                    "Error: Unable to convert wallet balance to float."
                                )

                        except Exception as err:
                            wallet_balance = 0.0
                            print(
                                f"ERROR -> {response.get('retCode')}: {response.get('retMsg')}"
                            )
                            print(f"Main error: {err}")

                        try:
                            # Построение параметров ордера
                            order_link_id = f'{ticker}:{strategy.last_price}-{strftime("%a, %d %b %Y", localtime())}.'

                            coff_position = 0.45 / 100

                            qty_usdt = (
                                wallet_balance * coff_position
                            ) * Params.Param_RiskLimit
                            qty_ticker = qty_usdt / strategy.last_price

                            qty_ticker = min(
                                max(qty_ticker, float(ticker_info["minOrderQty"])),
                                float(ticker_info["maxOrderQty"]),
                            )
                            if qty_ticker > 0:
                                qty_ticker = round(qty_ticker, 0)
                            else:
                                qty_ticker = round(qty_ticker, 4)

                            # Размещаем ордер
                            response = session.place_order(
                                category="linear",
                                symbol=ticker,
                                side=Params.Side.Buy,
                                orderType="Market",
                                qty=str(qty_ticker),
                                triggerBy="LastPrice",
                                timeInForce="GTC",
                                positionIdx=0,
                                takeProfit=str(
                                    strategy.get_tp_or_sl_value(
                                        Params.Side.TP,
                                        strategy.last_price,
                                        Params.Side.Buy,
                                    )
                                ),
                                stopLoss=str(
                                    strategy.get_tp_or_sl_value(
                                        Params.Side.SL,
                                        strategy.last_price,
                                        Params.Side.Buy,
                                    )
                                ),
                                tpTriggerBy="MarkPrice",
                                slTriggerBy="IndexPrice",
                                orderLinkId=order_link_id,
                                isLeverage=1,
                            )

                            # Проверяем ответ на создание ордера
                            try:
                                if response.get("retCode") == 0:
                                    print(
                                        f'{response["result"]["orderLinkId"]}\n{response}'
                                    )
                                    Log.info(
                                        f'{response["result"]["orderLinkId"]}\n{response}'
                                    )
                                else:
                                    raise ValueError(
                                        f"Order creation failed with code {response['retCode']}: {response['retMsg']}"
                                    )
                            except ValueError as response_error:
                                try:
                                    # Отменяем ордер в случае ошибки
                                    session.cancel_order(
                                        category="linear",
                                        symbol=ticker,
                                        orderId=order_link_id,
                                    )
                                    print(
                                        f"Canceled -> {response['retCode']}: {response['retMsg']}"
                                    )
                                    Log.error(
                                        f"Canceled -> {ticker} -> {response['retCode']}: {response['retMsg']}"
                                    )
                                except Exception as cancel_order_err:
                                    print(f"Error canceling order: {cancel_order_err}")
                                    Log.error(
                                        f"Error canceling order: {cancel_order_err}"
                                    )
                                raise response_error

                        except Exception as build_order_err:
                            print(f"Error building order params: {build_order_err}")
                            Log.error(f"Error building order params: {build_order_err}")
                            raise

                        strategy.peaks.clear()
                        strategy.SIGNAL = False
    except Exception as err:
        Log.error(f"Error -> {err}", exc_info=True)
        traceback.print_exc(file=sys.stderr)


# 1 5 15 30 (min)
# 60 120 240 (min)
# D (day)
# W (week)
# M (month)


def start():
    Ticker_Info = {}

    try:
        # Получение информации о доступных инструментах
        response: dict = session.get_instruments_info(
            category="linear",
            status="Trading",
        )

        result: dict = response.get("result")
        tickers = result.get("list")

        for symbol in tickers:
            try:
                # Получение информации о тикере
                response: dict = session.get_tickers(
                    category="linear", symbol=symbol.get("symbol")
                )
                result: dict = response.get("result")
                ticker: dict = result.get("list")[
                    0
                ]  # Получаем первый элемент из списка

                # Проверка волатильности
                if (
                    Trading_View.checkSymbol(symbol.get("symbol"))
                    and Params.Param_LowVolatilityPrcnt
                    < float(ticker.get("price24hPcnt", 0))
                    < Params.Param_HighVolatilityPrcnt
                ):
                    # Обновление информации о тикере
                    Ticker_Info.update(
                        {
                            symbol.get("symbol"): {
                                "leverage": symbol.get("leverageFilter").get(
                                    "maxLeverage"
                                ),
                                "minOrderQty": symbol.get("lotSizeFilter").get(
                                    "minOrderQty"
                                ),
                                "maxOrderQty": symbol.get("lotSizeFilter").get(
                                    "maxOrderQty"
                                ),
                            }
                        }
                    )
                    # Установка кредитного плеча
                    try:
                        response = session.set_leverage(
                            category="linear",
                            symbol=symbol.get("symbol"),
                            buyLeverage=str(
                                symbol.get("leverageFilter").get("maxLeverage")
                            ),
                            sellLeverage=str(
                                symbol.get("leverageFilter").get("maxLeverage")
                            ),
                        )
                    except Exception as set_leverage_err:
                        print(
                            f"Error setting leverage for {symbol.get('symbol')}: {set_leverage_err}"
                        )

            except Exception as ticker_err:
                print(f"Error processing ticker {symbol.get('symbol')}: {ticker_err}")

    except Exception as err:
        print(f"ERROR -> {response.get('retCode')}: {response.get('retMsg')}")
        print(f"Main error: {err}")

    print(Ticker_Info)
    return Ticker_Info  # Возвращаем Ticker_Info
    # ==========================================================================================


def start_websocket(ticker_info, argv):
    try:
        strategy = Triangle()
        ws = WebSocketClient("wss://stream.bybit.com/v5/public/linear", argv)
        ws.ws_app.on_message = partial(handle_kline, ticker_info, strategy)
        ws.run()
    except websocket.WebSocketConnectionClosedException as err:
        print(f"Соединение было закрыто: {err}")
        Log.error(f"Error -> {err}", exc_info=True)


def start_processes(tickers: dict):
    processes = []
    symbols = list(tickers.keys())
    try:
        for i in range(min(20, len(symbols))):  # Проверка на количество тикеров
            proc = Process(
                target=start_websocket,
                args=(
                    symbols[i],
                    [
                        "{}.{}.{}".format(
                            "some_subscription", "some_interval", symbols[i]
                        ),
                    ],
                ),
            )
            processes.append(proc)
            proc.start()

        # Теперь ждем завершения всех процессов
        for proc in processes:
            proc.join()
    except Exception as err:
        Log.error(f"Error -> {err}", exc_info=True)
        print(f"__main__  -> Произошла непредвиденная ошибка: {err}")


def close(processes):
    for proc in processes:
        if proc.is_alive():
            proc.terminate()
            proc.join()
            print("CLOSE ->", proc.name)


if __name__ == "__main__":
    Tickers = start()
    start_processes(Tickers)
