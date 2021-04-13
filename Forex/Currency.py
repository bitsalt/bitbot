from Forex.CurrencyPair import CurrencyPair

class Currency():
    def __init__(self, currency):
        self.currency = currency
        self.pairs = CurrencyPair()


    def getPairsList(self):
        if self.pairs != None:
            return self.pairs.getPairs(self.currency)
        return self.pairs

