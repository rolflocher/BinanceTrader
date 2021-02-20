from .TradeTransformer import TradeTransformer
from .TradeSQLService import TradeSQLService

class TradeLoader:

	service = TradeSQLService()

	# Expects database name 'name.db'
	def load(self, databaseName, limit = 100000):
		connection = self.service.createConnection(databaseName)
		with connection:
			trades = self.service.getTrades(connection, limit)
			transformer = TradeTransformer()
			return transformer.transform(trades)
