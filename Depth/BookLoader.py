from SQLService import SQLService

import json

class BookLoader:

	def __init__(self, selector = None, transformer = None):
		if selector == None:
			selector = BookSelector()
		if transformer == None:
			transformer = BookTransformer()
		self.selector = selector
		self.transformer = transformer

	def load(self, databaseName, limit = None, after = None):
		books = self.selector.select(databaseName, limit, after)
		return self.transformer.transform(books)
		
class BookSelector:

	def __init__(self, service = None):
		if service == None:
			service = SQLService()
		self.service = service

	def select(self, databaseName, limit, after):
		conn = self.service.createConnection(databaseName)
		with conn:
			print(self.service.getRowCount('books'))
			return self.service.get('books', limit, after)

class BookTransformer:

	def transform(self, dtos):
		books = []
		for dto in dtos:
			book = {
				'time': dto[0],
				'lastId': dto[1],
				'bids': [[float(x[0]), float(x[1])] for x in json.loads(dto[2])],
				'asks': [[float(x[0]), float(x[1])] for x in json.loads(dto[3])]
			}
			books.append(book)
		return books
