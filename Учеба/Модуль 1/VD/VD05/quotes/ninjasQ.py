from http.client import responses

import requests
from typing import Dict


class Ninjas:
	def __init__(self):
		self.api_url = 'https://api.api-ninjas.com/v1/quotes'
		self.api_key = '5Oi910DZmwQh2bo+T1uVqw==vRW4t08SqzkV0ofn'

	def __connect(self):
		self.response = requests.get(
			self.api_url,
			headers={'X-Api-Key': self.api_key}
		)

		if self.response.status_code != requests.codes.ok:
			self.response = None

	def quote(self) -> Dict[str, str]:
		self.__connect()
		if self.response and self.response.status_code == 200:
			data = self.response.json()
			return {
				"author": data[0].get("author", "Unknown"),
				"quote": data[0].get("quote", ""),
			}

		return {}
