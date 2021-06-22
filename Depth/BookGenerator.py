
from Depth.DepthLoader import DepthLoader
from SQLService import SQLService

import copy
import json

class BookGenerator:

	def __init__(self, loader = None):
		if loader == None:
			loader = DepthLoader()
		self.loader = loader
	
	def generate(self, diffs, seed):
		service = SQLService()
		conn = service.createConnection('socketrnn.db')
		with conn:
			service.drop('books')
			service.createTable('books')
			book = dict(seed)
			count = 0
			for diff in diffs:
				if diff['lastId'] <= book['lastId']:
					continue
				count += 1
				newBook = self.applyChange(diff, copy.deepcopy(book))
				book = newBook
				service.insert('books', (book['time'], book['lastId'], json.dumps(book['bids']), json.dumps(book['asks'])))
				print("\rGenerating book", count, "of", len(diffs)-1, end="")
			print("Length of books", service.getRowCount('books'))
			
	def applyChange(self, diff, book):
		for bd in diff['bids']:
			curIndex = 0
			for bid in book['bids']:
				if float(bd[0]) == float(bid[0]):
					if float(bd[1]) == 0:
						try:
							del book['bids'][curIndex]
						except:
							print("Failed to remove")
					else:
						book['bids'][curIndex][1] = bd[1]
					break
				elif float(bd[0]) < float(bid[0]):
					curIndex = curIndex + 1
					continue
				else:
					if not float(bd[1]) == 0:
						book['bids'].insert(curIndex, bd)
					break
			if curIndex == len(book['bids']):
				if not float(bd[1]) == 0:
					book['bids'].insert(curIndex, bd)
		for ad in diff['asks']:
			curIndex = 0
			for ask in book['asks']:
				if float(ad[0]) == float(ask[0]):
					if float(ad[1]) == 0:
						try:
							del book['asks'][curIndex]
						except:
							print("Failed to remove")
					else:
						book['asks'][curIndex][1] = ad[1]
					break
				elif float(ad[0]) > float(ask[0]):
					curIndex = curIndex + 1
					continue
				else:
					if not float(ad[1]) == 0:
						book['asks'].insert(curIndex, ad)
					break
			if curIndex == len(book['asks']):
				if not float(ad[1]) == 0:
					book['asks'].insert(curIndex, ad)
		book['time'] = diff['time']
		book['lastId'] = diff['lastId']
		return book
