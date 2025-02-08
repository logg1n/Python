import os
from time import localtime, strftime
import socket
import sys
import wallet as wl
import logging
import traceback

# Получаем абсолютный путь к директории, где находится этот скрипт
dir_path = os.path.dirname(os.path.realpath(__file__))

# Создаем директорию 'logs', если она еще не существует
if not os.path.exists(os.path.join(dir_path, "logs")):
    os.makedirs(os.path.join(dir_path, "logs"))
if not os.path.isfile(os.path.join(dir_path, "logs", "wallet_server.log")):
    # Если файл не существует, вы можете создать его здесь
    open(os.path.join(dir_path, "logs", "wallet_server.log"), "w").close()
# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename=os.path.join(dir_path, "logs", "wallet_server.log"),
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)

# Создание и настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class EchoServer:
    def __init__(self, host="localhost", port=9090):
        self.host = host
        self.port = port
        self.w = wl.Wallet()

    def start(self):
        while True:  # Цикл для переподключения
            try:
                # Создаем сокет
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    # Привязываем сокет к адресу
                    s.bind((self.host, self.port))
                    # Переводим сокет в режим прослушивания
                    s.listen(10)
                    logging.info(f"Server is listening on {self.host}:{self.port}")

                    while True:
                        # Принимаем подключение
                        conn, addr = s.accept()
                        with conn:
                            logging.info(f"Connected by {addr}")
                            print(f"Connected by {addr}")

                            while True:
                                # Принимаем данные
                                data = conn.recv(1024).decode()
                                if not data:  # Если строка пустая, прерываем цикл
                                    break
                                if data == '$test':
                                    conn.sendall(f'Test connecting confirm{data.split(':')[-1]}'.encode())    
                                else:
                                    self.w.change(float(data))
                                # Отправляем данные обратно клиенту
                                conn.sendall(str(self.w.get_balance()).encode())
            except ConnectionResetError:
                logging.error("Connection lost. Attempting to reconnect...")
                continue  # Переходим к началу цикла для переподключения
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                # Ничего не делаем и продолжаем работу
                continue

if __name__ == "__main__":
    server = EchoServer()
    try:
        server.start()
    except KeyboardInterrupt:
        logging.info(f"Server stopped. {strftime("%a, %d %b %Y %H:%M:%S ", localtime())}")
        traceback.print_exc(file=sys.stderr)
