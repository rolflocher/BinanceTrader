
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
