
from Strategy.AStrategy_v2 import AStrategy_v2, StrategyDataSource
from Strategy.MACross_v2 import MACross_v2
from Plan.APlan_v2 import APlan_v2
from Plan.LongTrailingStopPlan_v2 import LongTrailingStopPlan_v2

from ComboLoader import ComboLoader

from Plan.Position import Position
from Plan.Order import Order

import copy

class Tester:

	def __init__(self, strategy: AStrategy_v2, plan: APlan_v2):
		self.strategy = strategy
		self.plan = plan
		self.positions = []
		self.orders = {}
		self.base = 100
		
	def test(self):
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
		curTime = int(curTime // (length * 1000 * 60) * (length * 1000 * 60)) + (length * 1000 * 6)
		
		while curTime + interval * 1000 < finalTime:
			#buffer all data sources
			curTime += interval * 1000
			minTime = curTime - length * 1000
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
							self.checkForSell(info[maxIndexes[symbol][type]])
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
			lastPrice = 0
			for symbol, types in data.items():
				slice[symbol] = {}
				for type, info in types.items():
					slice[symbol][type] = data[symbol][type][minIndexes[symbol][type]:maxIndexes[symbol][type]]
					# todo build last price dict from APlan.getTradeSymbols
					if type == StrategyDataSource.AGGTRADES:
						lastPrice = data[symbol][type][maxIndexes[symbol][type]]['p']
			
			lead = self.strategy.evaluate(slice, curTime/1000)
			orderReqs = self.plan.plan(lead, self.positions, self.orders, self.base)
			for orderReq in orderReqs:
				if orderReq.type == "MARKET":
					position = Position({
						"s": orderReq.symbol,
						"pa": orderReq.baseAmount/lastPrice,
						"ep": lastPrice,
						"ps": orderReq.positionSide,
						"cr": 0
					})
					self.positions.append(position)
					self.base -= orderReq.baseAmount
					print("Placing buy order at", lastPrice)
				if orderReq.type == "TRAILING_STOP_MARKET":
					order = Order({
						"o": orderReq.type,
						"i": fakeOrderId,
						"s": orderReq.symbol,
						"T": 0,
						"q": orderReq.baseAmount/lastPrice,
						"z": 0,
						"ap": lastPrice,
						"S": "SELL",
						"ps": "LONG",
						"cr": orderReq.priceRate,
						"sp": lastPrice * (1-orderReq.priceRate),
						"R": True
					})
					self.orders[fakeOrderId] = order
					fakeOrderId += 1
					
	def checkForSell(self, trade):
		orderRemoveIds = []
		positionRemoveIndexes = []
		for id, order in self.orders.items():
			if order.type == "TRAILING_STOP_MARKET":
				if order.positionSide == "LONG":
					if float(trade["p"]) < order.stopPrice:
						orderRemoveIds.append(id)
						self.base += order.stopPrice * order.quantity
						positionIndex = 0
						for position in self.positions:
							if position.positionSide == "LONG":
								position.quantity -= order.quantity
								if position.quantity < 0.0001:
									positionRemoveIndexes.append(positionIndex)
									print("Selling position at", order.stopPrice, "base now", self.base)
									break
							positionIndex += 1
					elif float(trade["p"]) > order.stopPrice / (1 - order.priceRate):
						order.stopPrice = float(trade["p"]) * (1 - order.priceRate)
		for id in orderRemoveIds:
			del self.orders[id]
		if len(positionRemoveIndexes) > 0:
			self.positions = [i for j, i in enumerate(self.positions) if j not in positionRemoveIndexes]
			
strategy = MACross_v2().setParams([16, 10, 10, "btcusdt", 60])
plan = LongTrailingStopPlan_v2().setParams([0.003, "btcusdt"])
tester = Tester(strategy, plan)
tester.test()
