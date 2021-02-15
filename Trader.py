from Strategy.AStrategy_v2 import AStrategy_v2
from Strategy.MACross_v2 import MACross_v2
from .AStrategy_v2 import StrategyDataSource
from Plan.APlan_v2 import APlan_v2
from Plan.LongTrailingStopPlan_v2 import LongTrailingStopPlan_v2
from Plan.Position import Position
from Plan.Order import Order

from WebsocketService import WebsocketService

import websockets
import requests
import hashlib
import asyncio
import time
import hmac

class KlineTrader:

	def __init__(self, symbol, interval, strategy, plan: APlan_v2):
		self.symbol = symbol
		self.interval = interval
		self.strategy = strategy
		self.plan = plan
		
		self.positions = {}
		self.orders = {}
		self.base = None
		self.apiKey = "V6lHOnJWwmCDmNuhQAJvUOSCJpBkpt7Kd2ZGVRTWVMjYjssyRBzYjRBmr3ZbE4y2"
		self.secretKey = "o8y08esS2SRQnPi4nzzqDZ8QfvbB7GzHccbrcMZMassuxnKbawKv5IVMPG8pkD6b"
		self.service = WebsocketService()
		self.tradeBuffer = []
		self.depthBuffer = []
		
		listenKey = self.getListenKey()
		
		sources = self.strategy.getDataSources()
		for key, source in sources:
			for type in source:
				if type == StrategyDataSource.Trades:
					loop.create_task(self.service.open("wss://fstream.binance.com/ws/btcusdt@aggTrade", self.recieveTradeData))
		loop = asyncio.get_event_loop()
#		loop.create_task(self.service.open("wss://fstream.binance.com/ws/" + listenKey, self.recieveUserData)
#		loop.create_task(self.service.open("wss://fstream.binance.com/ws/btcusdt@aggTrade", self.recieveTradeData))
		loop.create_task(self.service.open("wss://fstream.binance.com/ws/btcusdt@depth", self.recieveDepthData))
		loop.create_task(self.execute())
		loop.run_forever()
		
	def recieveData(self, msg):
		self.dataBuffer[msg['s']['e']].append(msg)
				
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

	def execute(self):
		# sync up system clock
		loader = KlineLoader()
		length = self.strategy.getMinLength()
		while True:
			klines = loader.load(self.symbol, self.interval, length, True)
			lead = self.strategy.evaluate(klines)
			orders = self.plan.trade(klines, self.positions)
			for order in orders:
				# place order
				print()
			

strategy = MACross().setParams([16, 10])
plan = LongTrailingStopPlan().setParams([0.3])
trader = KlineTrader("BTCUSDT", "1m", strategy, plan)
#trader.execute()
