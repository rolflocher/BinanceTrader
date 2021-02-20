
class Position:
	def __init__(self, json):
		self.symbol = json["s"]
		self.quantity = json["pa"]
		self.price = json["ep"]
		self.positionSide = json["ps"]
		self.accRealized = json["cr"]
			
#	def __init__(self, quantity, price, side, positionSide, type, priceRate, trailingMark = None):
#		self.quantity = quantity
#		self.price = price
#		self.side = side
#		self.positionSide = positionSide
#		self.type = type
#		self.priceRate = priceRate
#		self.trailingMark = trailingMark
			
