from .SQLService import SQLService

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
