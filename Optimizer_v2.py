
from Strategy.AStrategy_v2 import AStrategy_v2
from Strategy.MACross_v2 import MACross_v2
from Strategy.AStrategy_v2 import StrategyDataSource
from Plan.APlan_v2 import APlan_v2
from Plan.LongTrailingStopPlan_v2 import LongTrailingStopPlan_v2
from Plan.Position import Position
from Plan.Order import Order
from Trade.TradeLoader import TradeLoader
from Tester import Tester

import copy

class Optimizer_v2:

	def __init__(self, strategy: AStrategy_v2, plan: APlan_v2):
		self.strategy = strategy
		self.plan = plan
		
	def execute(self):
		bestEnd = 0
		bestStratParams = []
		bestPlanParams = []
		stratPerms = self.strategy.getPerms()
		for stratPerm in stratPerms:
			if not self.strategy.validateParams(stratPerm):
				continue
			self.strategy.setParams(stratPerm)
			planPerms = self.plan.getPerms()
			for planPerm in planPerms:
				self.plan.setParams(planPerm)
				base = 100
				positions = []
				orders = {}
				delta = self.strategy.getMinTime()
				fakeOrderId = 0
				
				# Need to load data based on data requirements of strategy
				# Need to format data based on data requirements
				
#				model = {}
#				modelSlice = {}
				requirements = self.strategy.getDataRequirements()
#				for symbol, req in requirements.items():
#					for type in req:
#						model[symbol][req] = TradeLoader().load('aggTrades.db')
				trades = TradeLoader().load('aggTrades.db', 10000)
				
				minIndex = 0
				maxIndex = 0
				minTime = trades[0]["T"]
				maxTime = trades[0]["T"]
				tradeBuffer = []
				while True:
					minTrade = trades[minIndex]
					maxTrade = trades[maxIndex]
					maxTime += delta
					if maxTime > trades[-1]["T"]:
						break
					while minTrade["T"] < minTime:
						minTrade = trades[minIndex]
						minIndex += 1
					while maxTrade["T"] < maxTime:
						maxTrade = trades[maxIndex]
						maxIndex += 1
						base -= self.checkForSell(maxTrade, orders, positions)
					maxIndex -= 1
					maxTrade = trades[maxIndex]
					print(time.time() - maxTrade["T"])
					minTime += delta
					tradesSlice = trades[minIndex:maxIndex]
					lead = self.strategy.evaluate(copy.deepcopy({"btcusdt": {StrategyDataSource.AGGTRADES: tradesSlice}}), maxTrade["T"])
					orderReqs = self.plan.plan(lead, positions, orders, base)
					for order in orderReqs:
						print(order)
						if orderReq.type == "MARKET":
							position = Position({
								"s": orderReq.symbol,
								"pa": orderReq.baseAmount/maxTrade["p"],
								"ep": maxTrade["p"],
								"ps": orderReq.positionSide,
								"cr": 0
							})
							positions.append(position)
							base -= orderReq.baseAmount
							print("Placing buy order at", maxTrade["p"])
						if orderReq.type == "TRAILING_STOP_MARKET":
							order = Order({
								"o": orderReq.type,
								"i": fakeOrderId,
								"s": orderReq.symbol,
								"T": 0,
								"q": orderReq.baseAmount/maxTrade["p"],
								"z": 0,
								"ap": maxTrade["p"],
								"S": "SELL",
								"ps": "LONG",
								"cr": orderReq.priceRate,
								"sp": maxTrade["p"] * (1-orderReq.priceRate),
								"R": True
							})
							orders[fakeOrderId] = order
							fakeOrderId += 1
				print(base)

strategy = MACross_v2().setParamRanges([range(15, 16), range(10, 11), [10], ["btcusdt"], [1]])
plan = LongTrailingStopPlan_v2().setParamRanges([[x * 0.1 for x in range(3, 4)], ["btcusdt"]])
optimizer = Optimizer_v2(strategy, plan)

optimizer.execute()
