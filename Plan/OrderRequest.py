
class OrderRequest:
	def __init__(self, type, symbol, quantity, price, side, positionSide, priceRate, reduceOnly):
		self.type = type
		self.symbol = symbol
		self.quantity = quantity
		self.price = price
		self.side = side
		self.positionSide = positionSide
		self.priceRate = priceRate
		self.reduceOnly = reduceOnly
