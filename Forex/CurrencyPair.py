
class CurrencyPair():
    def __init__(self):
        self.setPairs()

    def setPairs(self):
        self.pairs = {
            'USD': [
                'EUR_USD',
                'USD_CAD',
                'USD_CHF',
                'AUD_USD',
                'NZD_USD',
                'GBP_USD',
                'USD_JPY',
            ],
            'EUR': [
                'EUR_USD',
                'EUR_CAD',
                'EUR_AUD',
                'EUR_NZD',
                'EUR_CHF',
                'EUR_GBP',
            ],
        }

    def getPairs(self, baseCurrency):
        return self.pairs.get(baseCurrency)

    def getBaseCurrencies(self):
        return self.pairs.keys()


    def getAvailablePairs(self, baseCurrency):
        if baseCurrency in self.pairs.keys():
            return self.pairs.get(baseCurrency)
        else:
            return None

