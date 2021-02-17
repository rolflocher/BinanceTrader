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

class KlineTrader:

	def __init__(self, strategy: AStrategy_v2, plan: APlan_v2):
		self.strategy = strategy
		self.plan = plan
		
		self.positions = {}
		self.orders = {}
		self.dataBuffer = {}
		self.base = None
		self.apiKey = "V6lHOnJWwmCDmNuhQAJvUOSCJpBkpt7Kd2ZGVRTWVMjYjssyRBzYjRBmr3ZbE4y2"
		self.secretKey = "o8y08esS2SRQnPi4nzzqDZ8QfvbB7GzHccbrcMZMassuxnKbawKv5IVMPG8pkD6b"
		self.service = WebsocketService()
		
		self.base = self.getBalance()
		listenKey = self.getListenKey()
		
		loop = asyncio.get_event_loop()
		loop.create_task(self.service.open("wss://fstream.binance.com/ws/" + listenKey, self.recieveUserData))
		
		sources = self.strategy.getDataSources()
		for key, source in sources.items():
			self.dataBuffer[key] = {}
			for type in source:
				self.dataBuffer[key][type] = []
				loop.create_task(self.service.open("wss://fstream.binance.com/ws/" + key + "@" + type, self.recieveData))
		
		loop.create_task(self.execute())
		loop.run_forever()
		
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
				self.positions = {}
				for positionDto in msg['a']['P']:
					position = Position(positionDto)
					self.positions = position
		
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
			orders = self.plan.plan(lead, self.positions, self.orders, self.base)
			for order in orders:
				# place order
				print()
				print(order)
				print()

strategy = MACross_v2().setParams([16, 10, 1, "btcusdt"])
plan = LongTrailingStopPlan_v2().setParams([0.3, "btcusdt"])
trader = KlineTrader(strategy, plan)
