
import asyncio
import websockets
import time
import json

class WebsocketService:

	async def open(self, endpoint, callback):
		async with websockets.connect(endpoint) as websocket:
			lastPong = time.time()
			while True:
				subcriptionResponse = await websocket.recv()
				callback(json.loads(subcriptionResponse))
				currentTime = time.time()
				if currentTime - lastPong > 60:
					await websocket.pong()
					lastPong = currentTime
