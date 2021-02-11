from .AStrategy import AStrategy
from typing import Optional

import pandas as pd

class MACross(AStrategy):

	def evaluate(self, klines) -> Optional[bool]:
		series = self.parseSeries(klines)
		slowMA = self.getMA(series, self.params[0])
		fastMA = self.getMA(series, self.params[1])
		if fastMA[-2] < slowMA[-2] and fastMA[-1] > slowMA[-1]:
			return True
		elif fastMA[-2] > slowMA[-2] and fastMA[-1] < slowMA[-1]:
			return False
		else:
			return None
			
	def getMinLength(self) -> int:
		return self.params[0] + 1
		
	def validateParams(self, params):
		return params[0] > params[1]
			
	def parseSeries(self, klines) -> list:
		series = []
		for kline in klines:
			series.append(kline.close)
		return series
			
	def getMA(self, series: list, length: int) -> list:
		series = pd.Series(series).rolling(window=length).mean().iloc[length-1:].values
		return list(series)
