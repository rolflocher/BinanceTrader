
class Position:
	def __init__(self, json):
#		self.symbol = json["symbol"]
#		self.time = json["updateTime"]
		self.quantity = json["executedQty"]
		self.price = json["price"]
		self.side = json["side"]
		self.positionSide = json["positionSide"]
		self.type = json["type"]
		self.priceRate = json["priceRate"]
		self.trailingMark = None
		if "trailingMark" in json:
			self.trailingMark = json["trailingMark"]
