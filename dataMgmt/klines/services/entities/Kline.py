
class APersistableEntity:
	def setIdentity(self, id):
		self.identity = id

	def getIdentity(self):
		return self.identity

class Kline(APersistableEntity):
	def setOpen(open):
		self.open = open

	def setHigh(high):
		self.high = high

	def setLow(low):
		self.low = low

	def setClose(close):
		self.close = close

	def setVolume(volume):
		self.volume = volume

	def getOpen():
		return self.open

	def getHigh():
		return self.high

	def getLow():
		return self.low

	def getClose():
		return self.close

	def getVolume():
		return self.volume