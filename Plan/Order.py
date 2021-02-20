
class Order:

	def __init__(self, json):
		self.id = json["i"]
		self.symbol = json["s"]
		self.time = json["T"]
		self.quantity = json["q"]
		self.filledQuantity = json["z"]
		self.price = json["ap"]
		self.side = json["S"]
		self.positionSide = json["ps"]
		self.type = json["o"]
		self.priceRate = json["cr"]
		self.stopPrice = json["sp"]
		self.reduceOnly = json["R"]
