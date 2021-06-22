
from SQLService import SQLService

import json

class DepthLoader:

	def __init__(self, selector = None, transformer = None):
		if selector == None:
			selector = DepthSelector()
		if transformer == None:
			transformer = DepthTransformer()
		self.selector = selector
		self.transformer = transformer

	def load(self, databaseName, limit = None):
		diffs, seed = self.selector.select(databaseName, limit)
		return self.transformer.transform(diffs, seed)

class DepthSelector:

	def __init__(self, service = None):
		if service == None:
			service = SQLService()
		self.service = service

	def select(self, databaseName, limit):
		conn = self.service.createConnection(databaseName)
		with conn:
			diffs = self.service.getDepthDiffs(limit)
			seed = self.service.getBookSeeds(1)[0]
			return diffs, seed

class DepthTransformer:
	
	def transform(self, diffs, seed):
		diffDtos = []
		for diff in diffs:
			diffDto = {
				'time': diff[0],
				'firstId': diff[1],
				'lastId': diff[2],
				'bids': json.loads(diff[3]),
				'asks': json.loads(diff[4])
			}
			diffDtos.append(diffDto)
		seedDto = {
			'lastId': seed[0],
			'bids': json.loads(seed[1]),
			'asks': json.loads(seed[2])
		}
		return diffDtos, seedDto
