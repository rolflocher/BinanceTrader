
from Trade.TradeLoader import TradeLoader
from Depth.DepthLoader import DepthLoader
from Depth.BookGenerator import BookGenerator
from Strategy.AStrategy_v2 import StrategyDataSource

class ComboLoader:
	def __init__(self):
		self.tradeLoader = None
		self.depthLoader = None
		self.bookGenerator = None
		
	def getTradeLoader(self):
		if self.tradeLoader == None:
			self.tradeLoader =  TradeLoader()
		return self.tradeLoader
	
	def getDepthLoader(self):
		if self.depthLoader == None:
			self.depthLoader =  DepthLoader()
		return self.depthLoader
		
	def getBookGenerator(self):
		if self.bookGenerator == None:
			self.bookGenerator =  BookGenerator()
		return self.bookGenerator

	def load(self, databaseName, reqs):
		model = {}
		for symbol, types in reqs.items():
			model[symbol] = {}
			for type in types:
				if type == StrategyDataSource.AGGTRADES:
					model[symbol][type] = self.getTradeLoader().load(databaseName)
				elif type == StrategyDataSource.DEPTH:
					diffs, seed = self.getDepthLoader().load(databaseName)
					model[symbol][type] = self.getBookGenerator().generate(diffs, seed)
		return model

				
