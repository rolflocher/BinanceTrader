from .Kline import Kline

class KlineTransformer:

	def transform(self, json):
		klines = []
		for obj in json:
			klines.append(Kline(obj))
		return klines
