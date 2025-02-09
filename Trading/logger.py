import os
import logging
from datetime import datetime
from time import strftime, localtime
import locale


class Support:

    @staticmethod
    def set_logger() -> logging.Logger:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        date_folder = datetime.now().strftime("%Y-%m-%d")
        folder = os.path.join(dir_path, f"logs/trade/{date_folder}")
        if not os.path.exists(folder):
            os.makedirs(folder)

        file = f"logger"

        if not os.path.exists(folder):
            os.makedirs(folder)
        if not os.path.isfile(os.path.join(folder, f"{file}.log")):
            open(os.path.join(folder, f"{file}.log"), "w").close()

        logging.basicConfig(
            level=logging.INFO,
            filename=os.path.join(folder, f"{file}.log"),
            filemode="w",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        logger = logging.getLogger(file)
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
