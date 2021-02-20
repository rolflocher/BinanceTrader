
from Strategy.AStrategy_v2 import AStrategy_v2, StrategyDataSource
from Strategy.MACross_v2 import MACross_v2
from Plan.APlan_v2 import APlan_v2
from Plan.LongTrailingStopPlan_v2 import LongTrailingStopPlan_v2

from ComboLoader import ComboLoader

#from Strategy.AStrategy_v2 import StrategyDataSource

from Plan.Position import Position
from Plan.Order import Order

import copy

class Tester:

	def __init__(self, strategy: AStrategy_v2, plan: APlan_v2):
		self.strategy = strategy
		self.plan = plan
		
	def test(self):
		base = 100
		positions = []
		orders = {}
		fakeOrderId = 0
		
		length = self.strategy.getMinTime() # sec
		interval = self.strategy.getRefreshInterval() # sec
		reqs = self.strategy.getDataSources()

		data = ComboLoader().load('socketrnn.db', reqs)
		for (symbol, types) in data.items():
			for type in types:
				print(symbol, type, len(data[symbol][type]))
		minIndexes = {}
		maxIndexes = {}
		curTime = 0 # ms
		finalTime = 0 # ms
		for symbol, types in data.items():
			minIndexes[symbol] = {}
			maxIndexes[symbol] = {}
			for type, info in types.items():
				minIndexes[symbol][type] = 0
				maxIndexes[symbol][type] = 0
				if type == StrategyDataSource.AGGTRADES:
					curTime = int(info[0]['T'])
					finalTime = int(info[-1]['T'])
					break
				elif type == StrategyDataSource.DEPTH:
					curTime = int(info[0]['E'])
					finalTime = int(info[-1]['E'])
					break
		curTime = int(curTime // (interval * 1000 * 60) * (interval * 1000 * 60)) + (interval * 1000 * 6)
		
		while curTime < finalTime:
			#buffer all data sources
			curTime += interval * 1000
			minTime = curTime - interval * 1000
			for symbol, types in data.items():
				for type, info in types.items():
					while True:
						if type == StrategyDataSource.AGGTRADES:
							if info[minIndexes[symbol][type]]['T'] < minTime:
								minIndexes[symbol][type] += 1
							else:
								break
						elif type == StrategyDataSource.DEPTH:
							if info[minIndexes[symbol][type]]['E'] < minTime:
								minIndexes[symbol][type] += 1
							else:
								break
					while True:
						if type == StrategyDataSource.AGGTRADES:
							if info[maxIndexes[symbol][type]]['T'] < curTime:
								maxIndexes[symbol][type] += 1
							else:
								break
						elif type == StrategyDataSource.DEPTH:
							if info[maxIndexes[symbol][type]]['E'] < curTime:
								maxIndexes[symbol][type] += 1
							else:
								break
			slice = {}
			for symbol, types in data.items():
				slice[symbol] = {}
				for type, info in types.items():
					print(data[symbol][type][maxIndexes[symbol][type]]['T'] - data[symbol][type][minIndexes[symbol][type]]['T'])
					slice[symbol][type] = data[symbol][type][minIndexes[symbol][type]:maxIndexes[symbol][type]]
			
			
strategy = MACross_v2().setParams([16, 10, 10, "btcusdt", 60])
plan = LongTrailingStopPlan_v2().setParams([0.003, "btcusdt"])
tester = Tester(strategy, plan)
tester.test()
