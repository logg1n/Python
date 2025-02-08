from datetime import datetime
from functools import partial
from multiprocessing import Process
import json
import os
import sys
from threading import Timer
from time import localtime, sleep, strftime
import traceback
import websocket
from typing import List, Any

from web_socket import WebSocketClient
from session import Session
from support import Support
from triangle import Triangle

from params import Params

from CheckingLinearPerpetual import CheckingListLinearPerpetual
from key import KEY, SECRET


session = Session(KEY, SECRET)
Subs = [
    "tickers",
    "kline",
]

risk_limit = 5

dir_path = os.path.dirname(os.path.realpath(__file__))

date_folder = datetime.now().strftime("%Y-%m-%d")

trade_logs_path = os.path.join(dir_path, f"logs/trade/{date_folder}")
if not os.path.exists(trade_logs_path):
    os.makedirs(trade_logs_path)

log_filename = f"logger"
Log = Support.set_logger(trade_logs_path, log_filename)

# Глобальная переменная для отслеживания состояния WebSocket клиента
# websocket_active = False
# def run_sub_websocket():
#    global websocket_active
#
#    websocket_active = True
#    ws = WebSocketClient(
#        "wss://stream.bybit.com/v5/public/linear",
#        [
#            "{}.{}.{}".format("kline", 1, "BTCUSDT"),
#        ],
#    )
#    ws.ws_app.on_message = sub_handle_kline
#
#    # Устанавливаем флаг в True, указывая, что WebSocket клиент запущен
#    ws.run()
#    # После завершения работы WebSocket клиента, сбрасываем флаг
#    websocket_active = False
#
# def sub_handle_kline(ws, msg):
#    msg_json = json.loads(msg)
#    msg_dict = dict(msg_json)
#
#    if msg_dict.get("op"):
#        print(f"INFO -> {msg}")
#    elif str(msg_dict.get("topic")).split(".")[0] == "kline":
#        data_K = msg_dict.get("data", {})[0]
#        print("\t\t\t", datetime.now())
#        # if data_K["confirm"]:
#        # ws.close()


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
                temp = Support.set_indicator_values(
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

                        response = session.HTTP_Request(
                            "/v5/account/wallet-balance",
                            "GET",
                            "accountType=UNIFIED&coin=USDT",  # ###########
                        )
                        if response["retCode"] == 0:
                            balance = float(
                                response["result"]["list"][0]["coin"][0][
                                    "walletBalance"
                                ]
                            )
                        else:
                            balance = 0.0
                            print(
                                f"ERROR -> {response["retCode"]}: {response["retMsg"]}"
                            )
                            Log.error(
                                f"ERROR ->{ticker}-> {response["retCode"]}: {response["retMsg"]}"
                            )

                        #########################################################################################
                        # Process(target=run_sub_websocket).start()
                        #########################################################################################
                        order_link_id = f'{ticker}:{strategy.last_price}-{strftime("%a, %d %b %Y", localtime())}.'
                        order_params = Support.build_order(
                            ticker=ticker,
                            side=Params.Side.Buy,
                            price=strategy.last_price,
                            tp=strategy.get_tp_or_sl_value(
                                Params.Side.TP, strategy.last_price, Params.Side.Buy
                            ),
                            sl=strategy.get_tp_or_sl_value(
                                Params.Side.SL, strategy.last_price, Params.Side.Buy
                            ),
                            risk_limit=float(ticker_info["leverage"]),
                            balance=balance,
                            minQty=float(ticker_info["minOrderQty"]),
                            maxQty=float(ticker_info["maxOrderQty"]),
                            order_link_id=order_link_id,
                        )
                        response = session.HTTP_Request(
                            "/v5/order/create",
                            "POST",
                            order_params,
                        )
                        if response["retCode"] == 0:
                            print(
                                f'{response["result"]["orderLinkId"]}\n{order_params}'
                            )
                            Log.info(
                                f'{response["result"]["orderLinkId"]}\n{order_params}'
                            )
                        else:
                            session.HTTP_Request(
                                "/v5/order/cancel",
                                "POST",
                                json.dumps(
                                    {
                                        "category": "linear",
                                        "symbol": ticker,
                                        "orderLinkId": order_link_id,
                                    }
                                ),
                            )
                            print(
                                f"Canceled -> {response["retCode"]}: {response["retMsg"]}"
                            )
                            Log.error(
                                f"Canceled ->{ticker}-> {response["retCode"]}: {response["retMsg"]}"
                            )

                        strategy.peaks.clear()
                        strategy.SIGNAL = False
    except Exception as err:
        Log.error(f"Error -> {err}", exc_info=True)
        traceback.print_exc(file=sys.stderr)


def start_websocket(ticker_info, argv):
    try:
        strategy = Triangle()
        ws = WebSocketClient("wss://stream.bybit.com/v5/public/linear", argv)
        ws.ws_app.on_message = partial(handle_kline, ticker_info, strategy)
        ws.run()
    except websocket.WebSocketConnectionClosedException as err:
        print(f"Соединение было закрыто: {err}")
        Log.error(f"Error -> {err}", exc_info=True)


# 1 5 15 30 (min)
# 60 120 240 (min)
# D (day)
# W (week)
# M (month)


def start():
    Sussed_Ticker = []

    for k in CheckingListLinearPerpetual:
        response: dict = session.HTTP_Request(
            "/v5/market/tickers", "GET", "category=linear&symbol={}".format(k)
        )

        if response["retCode"] == 0:
            if (
                Params.Param_LowVolatilityPrcnt
                < float(response.get("result").get("list")[0]["price24hPcnt"])
                < Params.Param_HighVolatilityPrcnt
            ):
                Sussed_Ticker.append(k)
    print(Sussed_Ticker)
    Ticker_Info = {}
    # ==========================================================================================
    response: dict = session.HTTP_Request(
        "/v5/market/instruments-info", "GET", "category=linear"
    )

    if response["retCode"] == 0:
        for symbol in response.get("result")["list"]:
            symbol = List
            if symbol.get("symbol") not in Sussed_Ticker:

                continue
            if (
                symbol.get("status") == "Trading"
                and symbol.get("contractType") == "LinearPerpetual"
            ):

                Ticker_Info.update(
                    {
                        symbol.get("symbol"): {
                            "leverage": symbol.get("leverageFilter")["maxLeverage"],
                            "minOrderQty": symbol.get("lotSizeFilter")["minOrderQty"],
                            "maxOrderQty": symbol.get("lotSizeFilter")["maxOrderQty"],
                            #                                "qtyStep": symbol.get("lotSizeFilter")[
                            #                                    "qtyStep"
                            #                                ],
                        }
                    }
                )
    else:
        print(f"ERROR -> {response['retCode']}: {response['retMsg']}")

    for k in Sussed_Ticker:
        response = (
            session.HTTP_Request(
                "/v5/position/set-leverage",
                "POST",
                '{"category":"linear","symbol": "'
                + k
                + '",'
                + '"buyLeverage" :"'
                + str(Ticker_Info.get(k)["leverage"])
                + '",'
                + '"sellLeverage": "'
                + str(Ticker_Info.get(k)["leverage"])
                + '"}',
            ),
        )
    # ==========================================================================================
    processes = []
    try:
        for val in Sussed_Ticker[:35]:
            proc = Process(
                target=start_websocket,
                args=(
                    Ticker_Info.get(val),
                    [
                        "{}.{}.{}".format(Subs[1], Params.Param_Interval, val),
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
    return processes


def close(processes):
    for proc in processes:
        if proc.is_alive():
            proc.terminate()
            proc.join()
            print("CLOSE ->", proc.name)


if __name__ == "__main__":
    start()
