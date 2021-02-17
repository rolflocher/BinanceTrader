import sys
from abc import ABC
from typing import Optional

class AStrategy_v2(ABC):

	def evaluate(self, klines) -> Optional[bool]:
		pass
		
	def getRefreshInterval(self) -> float:
		pass
		
	def getMinTime(self) -> Optional[int]:
		pass
		
	def getDataSources(self) -> dict:
		pass
		
	def validateParams(self, params) -> bool:
		pass

	def setParams(self, params: list):
		self.params = params
		return self

	def getParams(self) -> list:
		return self.params

	def setParamRanges(self, ranges: list):
		self.paramRanges = ranges
		return self

	def getParamRanges(self) -> list:
		return self.paramRanges
		
	def getPerms(self) -> list:
		return self.genPerms(self.paramRanges)
		
	def genPerms(self, ranges) -> list:
		if len(ranges) == 1:
			temp = []
			for x in ranges[0]:
				temp.append([x])
			return temp
		perms = []
		for x in ranges[0]:
			for sub in self.genPerms(ranges[1:]):
				perms.append([x] + sub)
		return perms
	

class StrategyDataSource:
	TRADES = 'trades'
	AGGTRADES = 'aggTrade'
	DEPTH = 'depth'

