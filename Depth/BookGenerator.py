
from Depth.DepthLoader import DepthLoader

import copy

class BookGenerator:

    def __init__(self, loader = None):
        if loader == None:
            loader = DepthLoader()
        self.loader = loader
    
    def generate(self, diffs, seed):
        book = dict(seed)
        books = []
        for diff in diffs:
            if diff['lastId'] <= book['lastId']:
                continue
            newBook = self.applyChange(diff, copy.deepcopy(book))
            book = newBook
            books.append(newBook)
        return books
            
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
        return book
