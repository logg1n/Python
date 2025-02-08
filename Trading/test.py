from datetime import datetime, timedelta
import json
from web_socket import WebSocketClient
from multiprocessing import Process, freeze_support


# Глобальная переменная для отслеживания состояния WebSocket клиента
time = datetime.now() + timedelta(seconds=120)
proc = None


def run_websocket():
    ws = WebSocketClient(
        "wss://stream.bybit.com/v5/public/linear",
        [
            "{}.{}.{}".format("kline", 1, "BTCUSDT"),
        ],
    )
    ws.ws_app.on_message = test
    # Устанавливаем флаг в True, указывая, что WebSocket клиент запущен
    ws.run()
    # После завершения работы WebSocket клиента, сбрасываем флаг


def test(w, msg):
    msg_json = json.loads(msg)
    msg_dict = dict(msg_json)

    if msg_dict.get("op"):
        print(f"INFO -> {msg}")
    elif str(msg_dict.get("topic")).split(".")[0] == "kline":
        data_K = msg_dict.get("data", {})[0]
        print("\t\t\t", datetime.now())
        # if data_K["confirm"]:
        # w.close()


def handle_kline_temp(wst, msg):
    global proc

    try:
        msg_json = json.loads(msg)
        msg_dict = dict(msg_json)

        if msg_dict.get("op"):
            print(f"INFO -> {msg}")
        elif str(msg_dict.get("topic")).split(".")[0] == "kline":
            ticker = str(msg_dict.get("topic")).split(".")[-1]
            data_K = msg_dict.get("data", {})[0]
            print(datetime.now())
            if data_K["confirm"]:
                if proc is None or not proc.is_alive() or proc.name != "test":
                    # Запускаем новый процесс, если WebSocket клиент не активен
                    proc = Process(target=run_websocket, name="test").start()
                if datetime.now() < time:
                    proc.terminate()
                    proc.join()

    except Exception as err:
        print(f"Произошла ошибка: {err}")


def main():
    global websocket_active
    wst = WebSocketClient(
        "wss://stream.bybit.com/v5/public/linear",
        [
            "{}.{}.{}".format("kline", 5, "BTCUSDT"),
        ],
    )
    wst.ws_app.on_message = handle_kline_temp
    wst.run()


if __name__ == "__main__":
    freeze_support()  # Для Windows, если вы планируете создавать исполняемый файл
    main()
