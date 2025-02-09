import websocket

# from datetime import datetime
import json


class WebSocketClient:
    def __init__(self, url, argv=[]):
        self.url = url
        self.argv = argv
        self.ws_app = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_ping=self.on_ping,
            on_pong=self.on_pong,
            on_open=self.on_open,
        )

    def on_message(self, ws, message):
        #    # Преобразование сообщения в JSON
        #    message_json = json.loads(message)

        #    # Преобразование JSON в словарь
        #    message_dict = dict(message_json)
        #    print(message_dict)
        pass

    def on_error(self, ws, error):
        print(f"Ошибка: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"Соединение закрыто-> {close_status_code}: {close_msg}")

    def on_open(self, ws):
        print("Соединение установлено")
        # Вы можете отправить сообщение на сервер после установки соединения
        print({"op": "subscribe", "args": self.argv})
        ws.send(json.dumps({"op": "subscribe", "args": self.argv}))

    def on_pong(self, ws, message):
        #        print(f"pong received : {datetime.now().strftime("%d/%m/%Y %H:%M:%S")} : {message}")
        pass

    def on_ping(self, ws, message):
        #        print(f"pong received : {datetime.now().strftime("%d/%m/%Y %H:%M:%S")} : {message}")
        #        print("ping received")
        pass

    def run(self):
        #        websocket.enableTrace(True)
        self.ws_app.run_forever(
            ping_interval=20,
            ping_timeout=10,
            ping_payload=json.dumps({"req_id": "100001", "op": "ping"}),
        )
