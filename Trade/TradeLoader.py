from SQLService import SQLService

class TradeLoader:

	def load(self, databaseName, limit = None, after = None):
		trades = TradeSelector().select(databaseName, limit, after)
		return TradeTransformer().transform(trades)

class TradeSelector:

	def select(self, databaseName, limit, after):
		service = SQLService()
		conn = service.createConnection(databaseName)
		with conn:
			return service.get('aggTrades', limit, after)

class TradeTransformer:

    def transform(self, trades):
        tradeDtos = []
        for trade in trades:
            tradeDtos.append({
                "p": trade[0],
                "q": trade[1],
                "m": trade[2],
                "T": trade[3],
                "E": trade[4],
                "a": trade[5]
            })
        return tradeDtos
