
class Kline:
	def __init__(self, json):
		self.openTime = int(json[0])
		self.open = float(json[1])
		self.high = float(json[2])
		self.low = float(json[3])
		self.close = float(json[4])
		self.volume = float(json[5])
		self.closeTime = int(json[6])
		self.quoteAssetVolume = float(json[7])
		self.numberTrades = int(json[8])
		self.TBBAV = float(json[9])
		self.TBQAV = float(json[10])
