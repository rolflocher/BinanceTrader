
from Strategy.AStrategy import AStrategy
from Strategy.MACross import MACross
from Plan.APlan import APlan
from Plan.LongTrailingStopPlan import LongTrailingStopPlan
from Plan.Position import Position
from Kline.KlineLoader import KlineLoader

class Optimizer:
	def __init__(self, strategy: AStrategy, plan: APlan):
		self.strategy = strategy
		self.plan = plan
		
	def execute(self, klines):
		bestEnd = 0
		bestParams = []
		bestPlanParams = []
		perms = self.strategy.getPerms()
		for perm in perms:
			if not self.strategy.validateParams(perm):
				continue
			self.strategy.setParams(perm)
			planPerms = self.plan.getPerms()
			for planPerm in planPerms:
				self.plan.setParams(planPerm)
				base = 100
				positions = []
				length = self.strategy.getMinLength()
				for x in range(length, len(klines)):
					windowedKlines = klines[x - length : x]
					# check positions for trailing stop loss
					removeIndexes = []
	#				availableAssets = 0
					posCount = 0
					for position in positions:
						if position.type == "TRAILING_STOP_MARKET":
							if position.positionSide == "LONG":
								if windowedKlines[-1].low < position.trailingMark * ((100-position.priceRate) / 100):
									base += position.quantity * position.trailingMark * ((100-position.priceRate) / 100)
									removeIndexes.append(posCount)
									for i, subPosition in enumerate(positions):
										if subPosition.type == "MARKET":
											subPosition.quantity -= position.quantity
											if subPosition.quantity < 0.1:
												removeIndexes.append(i)
											break
								elif windowedKlines[-1].high > position.trailingMark:
									position.trailingMark = windowedKlines[-1].high
							#todo else
						posCount += 1
					positions = [i for j, i in enumerate(positions) if j not in removeIndexes]
					# check positions for stop loss / take profit
					# todo
					lead = self.strategy.evaluate(windowedKlines)
					orders = self.plan.trade(windowedKlines, positions, lead, base)
					# update positions and base from orders
					for order in orders:
						if order.type == "MARKET":
							position = Position({
								order.quantity,
								order.price,
								order.side,
								order.positionSide,
								order.type,
								order.priceRate
							})
							positions.append(position)
							base -= position.quantity * position.price
						elif order.type == "TRAILING_STOP_MARKET":
							position = Position({
								order.quantity,
								order.price,
								order.side,
								order.positionSide,
								order.type,
								order.priceRate,
								order.price
							})
							positions.append(position)
				for position in positions:
					if position.type == "MARKET":
						base += position.quantity * klines[-1].close
				if base > bestEnd:
					bestEnd = base
					bestParams = perm
					bestPlanParams = planPerm
					print("new best:", base, perm, bestPlanParams)

strategy = MACross().setParamRanges([range(100, 200), range(3, 100)])
#strategy = MACross().setParamRanges([range(5, 6), range(3, 4)])
plan = LongTrailingStopPlan().setParamRanges([[x * 0.1 for x in range(3, 20)]])
optimizer = Optimizer(strategy, plan)

klines = KlineLoader().load("BTCUSDT", "1m", 500, True)
optimizer.execute(klines)
