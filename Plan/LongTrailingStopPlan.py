from .APlan import APlan
from .Order import Order
from .Position import Position

class LongTrailingStopPlan(APlan):

	def __init__(self):
#		self.trailingStopPrice = None
		self.trailingStopPercent = None

	def trade(self, klines, positions, lead, base) -> list:
		if len(positions) == 0:
			if lead == True:
				self.trailingStopPercent = self.params[0]
#				self.trailingStopPrice = klines[-1].close * ((100 - self.trailingStopPercent) / 100)
				buyOrder = Order(
					"MARKET",
					base/klines[-1].close,
					klines[-1].close,
					"BUY",
					"LONG",
					None,
					False)
				trailingOrder = Order(
					"TRAILING_STOP_MARKET",
					base/klines[-1].close,
					klines[-1].close,
					"SELL",
					"LONG",
					self.trailingStopPercent,
					True)
				return [buyOrder, trailingOrder]
#		else:
#			if klines[-1].low < self.trailingStopPrice:
#				return Order()
#			if klines[-1].high * ((100 - self.trailingStopPercent) / 100) > self.trailingStopPrice:
#				self.trailingStopPrice = klines[-1].high * ((100 - self.trailingStopPercent) / 100)
			
		return []

	def validateParams(self, params) -> bool:
		return True
