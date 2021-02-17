from .AStrategy_v2 import AStrategy_v2
from .AStrategy_v2 import StrategyDataSource
from typing import Optional

import pandas as pd

# Params:
# 0: Length of slow MA (sec)
# 1: Length of fast MA (sec)
# 2: Refresh interval (sec)
# 3: MA symbol
# 4: Trade symbol
# 5: MA Interval (sec)

class MACross_v2(AStrategy_v2):

	def evaluate(self, data, time) -> Optional[bool]:
		trades = data[self.params[3]][StrategyDataSource.AGGTRADES]
		series = self.parseSeries(trades, time)
		slowMA = self.getMA(series, self.params[0])
		fastMA = self.getMA(series, self.params[1])
		print("\rSlow:", slowMA[-1], "Fast:", fastMA[-1], "Diff:", fastMA[-1] - slowMA[-1], end="")
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
		return {self.params[3]: [StrategyDataSource.AGGTRADES]}
		
	def validateParams(self, params):
		return params[0] > params[1]
			
	def parseSeries(self, trades, time) -> list:
		series = []
		for x in range(0, self.getMinTime()):
			if len(trades) == 0:
				if len(series) == 0:
					series.append(0)
				else:
					series.append(series[-1])
				continue
			series.append(0)
			while True:
				trade = trades.pop(0)
				if len(trades) == 0:
					series[-1] = float(trade['p'])
					break
				if float(trade['T'])/1000 < time - self.getMinTime() + x + 1:
					series[-1] = float(trade['p'])
				else:
					trades.insert(0, trade)
					break
		return series
			
	def getMA(self, series: list, length: int) -> list:
		series = pd.Series(series).rolling(window=length).mean().iloc[length-1:].values
		return list(series)
