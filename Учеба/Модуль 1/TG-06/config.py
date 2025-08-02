import os
from dotenv import load_dotenv


load_dotenv()

class Singleton(type):
	_instance= {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instance:
			instance = super().__call__(*args, **kwargs)
			cls._instance[cls] = instance
		return cls._instance[cls]

class Config(metaclass=Singleton):
	TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

	def __init__(self):
		if not self.TELEGRAM_TOKEN:
			raise ValueError("TELEGRAM_TOKEN не установлен в ..env")


config = Config()