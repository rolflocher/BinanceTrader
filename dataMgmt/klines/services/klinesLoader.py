import requests

class KlinesLoader:

    class Arguments:
        def __init__(self):
            self.interval = None
            self.pair = None
            self.limit = None

        def setInterval(self, interval):
            self.interval = interval

        def setPair(self, pair):
            self.pair = pair

        def setLimit(self, limit):
            self.limit = limit

        def getInterval(self):
            return self.interval

        def getPair(self):
            return self.pair

        def getLimit(self):
            return self.limit

    def load(self, args: Arguments):
        url = "https://api.binance.com/api/v3/klines"
        querystring = {
            "symbol": args.getPair(),
            "interval": args.getInterval(),
            "limit": args.getLimit()
        }
        response = requests.request("GET",url,params=querystring)
        json = response.json()
        print(json)

loader = KlinesLoader()
args = KlinesLoader.Arguments()
args.setInterval("1m")
args.setLimit(10)
args.setPair("BTCUSDT")
loader.load(args)