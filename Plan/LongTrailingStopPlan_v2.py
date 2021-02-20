from .APlan_v2 import APlan_v2
from .OrderRequest import OrderRequest

# Params:
# 0: Trailing stop callback rate
# 1: Trade symbol

class LongTrailingStopPlan_v2(APlan_v2):

	def getTradeSymbols(self) -> list:
		return [self.params[1]]

	def plan(self, lead, positions, orders, base) -> list:
		if len(positions) == 0:
			if lead == True:
				buyOrder = OrderRequest(
					"MARKET",
					self.params[1],
					base*0.5,
					None,
					"BUY",
					"LONG",
					None,
					False)
				trailingOrder = OrderRequest(
					"TRAILING_STOP_MARKET",
					self.params[1],
					base*0.5,
					None,
					"SELL",
					"LONG",
					self.params[0],
					True)
				return [buyOrder, trailingOrder]
		return []

	def validateParams(self, params) -> bool:
		return True
