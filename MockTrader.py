from Strategy.AStrategy_v2 import AStrategy_v2
from Strategy.MACross_v2 import MACross_v2
from Strategy.AStrategy_v2 import StrategyDataSource
from Plan.APlan_v2 import APlan_v2
from Plan.LongTrailingStopPlan_v2 import LongTrailingStopPlan_v2
from Plan.Position import Position
from Plan.Order import Order

from WebsocketService import WebsocketService

import websockets
import requests
import hashlib
import asyncio
import copy
import time
import hmac

class MockTrader:

	def __init__(self, strategy: AStrategy_v2, plan: APlan_v2):
		self.strategy = strategy
		self.plan = plan
		
		self.positions = []
		self.orders = {}
		self.dataBuffer = {}
		self.lastPrice = 0
		self.base = None
		self.apiKey = "V6lHOnJWwmCDmNuhQAJvUOSCJpBkpt7Kd2ZGVRTWVMjYjssyRBzYjRBmr3ZbE4y2"
		self.secretKey = "o8y08esS2SRQnPi4nzzqDZ8QfvbB7GzHccbrcMZMassuxnKbawKv5IVMPG8pkD6b"
		self.service = WebsocketService()
		
		self.base = self.getBalance()
		print("Starting balance:", self.base)
		listenKey = self.getListenKey()
		
		loop = asyncio.get_event_loop()
		loop.create_task(self.service.open("wss://fstream.binance.com/ws/" + listenKey, self.recieveUserData))
		
		for symbol in self.plan.getTradeSymbols():
			loop.create_task(
				self.service.open(
					"wss://fstream.binance.com/ws/" + symbol + "@aggTrade",
					self.recieveTradeData
				)
			)
		
		sources = self.strategy.getDataSources()
		for key, source in sources.items():
			self.dataBuffer[key] = {}
			for type in source:
				self.dataBuffer[key][type] = []
				loop.create_task(self.service.open("wss://fstream.binance.com/ws/" + key + "@" + type, self.recieveData))
		
		loop.create_task(self.execute())
		loop.run_forever()
		
	def recieveTradeData(self, msg):
		self.lastPrice = float(msg["p"])
		orderRemoveIds = []
		positionRemoveIndexes = []
		for id, order in self.orders.items():
			if order.type == "TRAILING_STOP_MARKET":
				if order.positionSide == "LONG":
					if float(msg["p"]) < order.stopPrice:
						orderRemoveIds.append(id)
						self.base += order.stopPrice * order.quantity
						positionIndex = 0
						for position in self.positions:
							if position.positionSide == "LONG":
								position.quantity -= order.quantity
								if position.quantity < 0.0001:
									positionRemoveIndexes.append(positionIndex)
									print("Selling position at", order.stopPrice, "base now", self.base)
									break
							positionIndex += 1
					elif float(msg["p"]) > order.stopPrice / (1 - order.priceRate):
						order.stopPrice = float(msg["p"]) * (1 - order.priceRate)
		for id in orderRemoveIds:
			del self.orders[id]
		if len(positionRemoveIndexes) > 0:
			self.positions = [i for j, i in enumerate(self.positions) if j not in positionRemoveIndexes]
		
	def recieveData(self, msg):
		self.dataBuffer[msg['s'].lower()][msg['e']].append(msg)
				
	def recieveUserData(self, msg):
		if msg['e'] == 'ORDER_TRADE_UPDATE':
			if msg['o']['x'] == 'EXPIRED' or msg['o']['x'] == 'CANCELED' or msg['o']['x'] == 'FILLED':
				del self.orders[msg['o']['i']]
			else:
				order = Order(orderDto)
				self.orders[msg['o']['i']] = order
		elif msg['e'] == 'ACCOUNT_UPDATE':
			self.base = float(msg['a']['B'][0]['wb'])
			if msg['a']['P']:
				self.positions = []
				for positionDto in msg['a']['P']:
					position = Position(positionDto)
					self.positions.append(position)
		
	def getListenKey(self):
		url = "https://fapi.binance.com/fapi/v1/listenKey"
		queryString = {"recvWindow": 60000, "timestamp": int(round(time.time() * 1000))}
		signature = hmac.new(self.secretKey.encode(), msg=str(queryString).encode(), digestmod=hashlib.sha256).hexdigest()
		queryString["signature"] = signature
		response = requests.request("POST", url, headers={"X-MBX-APIKEY": self.apiKey}, params=queryString)
		return response.json()["listenKey"]
		
	def getBalance(self):
		url = "https://fapi.binance.com/fapi/v2/account"
		query = {"timestamp": int(round(time.time() * 1000))}
		queryString = "timestamp=" + str(int(round(time.time() * 1000)))
		signature = hmac.new(self.secretKey.encode(), msg=str(queryString).encode(), digestmod=hashlib.sha256).hexdigest()
		query["signature"] = signature
		response = requests.request("GET", url, headers={"X-MBX-APIKEY": self.apiKey}, params=query)
		return float(response.json()["availableBalance"])

	async def execute(self):
		# sync up system clock
		minDelta = self.strategy.getMinTime()
		refreshInterval = self.strategy.getRefreshInterval()
		
		# continuously write buffers to larger trade list
		# at the refresh interval, chop off trades no longer needed
		# send the entire trimmed list of trades to the strategy
		# strategy will deal with converting the trades into 1s klines
		
		fakeOrderId = 0
		
		while True:
			await asyncio.sleep(refreshInterval)
			curTime = time.time()
			hasData = True
			for symbol, types in self.dataBuffer.items():
				for type, data in types.items():
					while True:
						if len(self.dataBuffer[symbol][type]) < 1:
							hasData = False
							break
						ref = self.dataBuffer[symbol][type].pop(0)
						dataTime = None
						if type == StrategyDataSource.AGGTRADES:
							dataTime = int(ref['T'])
						elif type == StrategyDataSource.DEPTH:
							dataTime = int(ref['E'])
						if curTime - minDelta > dataTime:
							continue
						else:
							self.dataBuffer[symbol][type].insert(0, ref)
							break
			if not hasData:
				continue
			lead = self.strategy.evaluate(copy.deepcopy(self.dataBuffer), curTime)
			orderReqs = self.plan.plan(lead, self.positions, self.orders, self.base)
			for orderReq in orderReqs:
				if orderReq.type == "MARKET":
					position = Position({
						"s": orderReq.symbol,
						"pa": orderReq.baseAmount/self.lastPrice,
						"ep": self.lastPrice,
						"ps": orderReq.positionSide,
						"cr": 0
					})
					self.positions.append(position)
					self.base -= orderReq.baseAmount
					print("Placing buy order at", self.lastPrice)
				if orderReq.type == "TRAILING_STOP_MARKET":
					order = Order({
						"o": orderReq.type,
						"i": fakeOrderId,
						"s": orderReq.symbol,
						"T": 0,
						"q": orderReq.baseAmount/self.lastPrice,
						"z": 0,
						"ap": self.lastPrice,
						"S": "SELL",
						"ps": "LONG",
						"cr": orderReq.priceRate,
						"sp": self.lastPrice * (1-orderReq.priceRate),
						"R": True
					})
					self.orders[fakeOrderId] = order
					fakeOrderId += 1

strategy = MACross_v2().setParams([16, 10, 10, "btcusdt", 60])
plan = LongTrailingStopPlan_v2().setParams([0.003, "btcusdt"])
trader = MockTrader(strategy, plan)
