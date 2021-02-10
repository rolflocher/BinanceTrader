from .KlineTransformer import KlineTransformer

import requests

class KlineLoader:

	def load(self, symbol, interval, limit, isFutures):
		json = self.request(symbol, interval, limit)
		return KlineTransformer().transform(json)
		
	def request(self, symbol, interval, limit, isFutures):
		url = None
		if isFutures:
			url = "https://testnet.binancefuture.com/fapi/v1/klines"
		else:
			url = "https://api.binance.com/api/v3/klines"
		querystring = {"symbol":symbol,"interval":interval, "limit": limit}
		response = requests.request("GET", url, headers={}, params=querystring)
		return response.json()
