from .AStrategy_v2 import AStrategy_v2
from .AStrategy_v2 import StrategyDataSource
from typing import Optional

import pandas as pd

# Params:
# 0: Length of slow MA
# 1: Length of fast MA
# 2: Refresh interval
# 3: MA symbol
# 4: Trade symbol

class MACross_v2(AStrategy_v2):

	def evaluate(self, data) -> Optional[bool]:
		trades = data[self.params[3]][StrategyDataSource.Trades]
		series = self.parseSeries(trades)
		slowMA = self.getMA(series, self.params[0])
		fastMA = self.getMA(series, self.params[1])
		if fastMA[-2] < slowMA[-2] and fastMA[-1] > slowMA[-1]:
			return True
		elif fastMA[-2] > slowMA[-2] and fastMA[-1] < slowMA[-1]:
			return False
		else:
			return None
			
	def getRefreshInterval(self) -> float:
		return self.params[2]
		
	def getMinTime(self) -> int:
		return self.params[0] + 1
		
	def getDataSources(self) -> dict:
		return {self.params[3]: [StrategyDataSource.Trades]}
		
	def getTradeSymbol(self) -> string:
		return self.params[4]
		
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
