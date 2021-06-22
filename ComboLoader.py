
from Trade.TradeLoader import TradeLoader
from Depth.BookLoader import BookLoader

class ComboLoader:
	def __init__(self):
		self.tradeLoader = None
		self.bookLoader = None

	def getTradeLoader(self):
		if self.tradeLoader == None:
			self.tradeLoader =  TradeLoader()
		return self.tradeLoader

	def getBookLoader(self):
		if self.bookLoader == None:
			self.bookLoader =  BookLoader()
		return self.bookLoader

	def load(self, databaseName, reqs, limit = None):
		model = {}
		after = None
		for symbol, types in reqs.items():
			model[symbol] = {}
			for type in types:
				if type == 'aggTrade':
					model[symbol][type] = self.getTradeLoader().load(databaseName, limit, after)
					if after == None:
						after = model[symbol][type][0]['T']
				elif type == 'depth':
					model[symbol][type] = self.getBookLoader().load(databaseName, limit, after)
					if after == None:
						after = model[symbol][type][0]['time']
		return model

