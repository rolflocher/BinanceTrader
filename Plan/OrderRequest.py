
class OrderRequest:
	def __init__(self, type, symbol, baseAmount, price, side, positionSide, priceRate, reduceOnly):
		self.type = type
		self.symbol = symbol
		self.baseAmount = baseAmount
		self.price = price
		self.side = side
		self.positionSide = positionSide
		self.priceRate = priceRate
		self.reduceOnly = reduceOnly

	def __str__(self):
		return str(self.type) + " " + str(self.symbol) + " " + str(self.baseAmount) + " " + str(self.price) + " " + str(self.side) + " " + str(self.positionSide) + " " + str(self.priceRate) + " " + str(self.reduceOnly)
