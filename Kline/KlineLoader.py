from .KlineTransformer import KlineTransformer

import requests

class KlineLoader:

	def load(self, symbol, interval, limit):
		json = self.request(symbol, interval, limit)
		return KlineTransformer().transform(json)
		
	def request(self, symbol, interval, limit):
		url = "https://api.binance.com/api/v3/klines"
		querystring = {"symbol":symbol,"interval":interval, "limit": limit}
		response = requests.request("GET", url, headers={}, params=querystring)
		return response.json()
