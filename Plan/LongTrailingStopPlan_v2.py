from .APlan_v2 import APlan_v2
from .Order import Order
from .Position import Position

class LongTrailingStopPlan_v2(APlan_v2):

	def plan(self, lead, positions, orders, base) -> list:
		if len(positions) == 0:
			if lead == True:
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
					self.params[0],
					True)
				return [buyOrder, trailingOrder]
		return []

	def validateParams(self, params) -> bool:
		return True
