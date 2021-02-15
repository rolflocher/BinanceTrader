
class Order:
	def __init__(self, type, quantity, price, side, positionSide, priceRate, reduceOnly):
		self.type = type
#		self.id = id
#		self.symbol = symbol
		self.quantity = quantity
		self.price = price
		self.side = side
		self.positionSide = positionSide
		self.priceRate = priceRate
		self.reduceOnly = reduceOnly

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
