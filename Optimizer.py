
from Strategy.AStrategy import AStrategy
from Strategy.MACross import MACross
from Kline.KlineLoader import KlineLoader

class Optimizer:
	def __init__(self, strategy: AStrategy):
		self.strategy = strategy
		
	def execute(self, klines):
#
#		if len(klines) < length:
#			print("Not enough klines supplied to strategy")
#			return
		
		bestEnd = 0
		bestParams = []
		perms = self.strategy.getPerms()
		for perm in perms:
			if not self.strategy.validateParams(perm):
				continue
			self.strategy.setParams(perm)
			base = 100
			position = None
			inAt = 0
			length = self.strategy.getMinLength()
			for x in range(length, len(klines)):
				lead = self.strategy.evaluate(klines[x - length : x])
				if position == None:
					if lead == True:
						inAt = klines[x].close
						position = True
					else:
						inAt = klines[x].close
						position = False
				elif position == True:
					if lead == False:
						base = base * ((klines[x].close / inAt) - 0.001)
						position = None
				else:
					if lead == True:
						base = base * ((inAt / klines[x].close) - 0.001)
						position = None
			if base > bestEnd:
				bestEnd = base
				bestParams = perm
				print("new best:", base, perm)

strategy = MACross().setParamRanges([range(5, 40), range(3, 20)])
optimizer = Optimizer(strategy)

klines = KlineLoader().load("BTCUSDT", "1m", 1000)
optimizer.execute(klines)
