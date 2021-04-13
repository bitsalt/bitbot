import unittest
from Forex.CurrencyPair import CurrencyPair
from Forex.Currency import Currency

class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        self.currency = None

    def test_canCreateCurrency(self):
        self.currency = Currency('USD')
        self.assertIsInstance(self.currency, Currency)
        self.assertEqual(self.currency.currency, 'USD')


    def test_canGetCurrencyPair(self):
        usd = Currency('USD')
        knownPairs = [
                'EUR_USD',
                'USD_CAD',
                'USD_CHF',
                'AUD_USD',
                'NZD_USD',
                'GBP_USD',
                'USD_JPY'
            ]
        pairList = usd.getPairsList()
        self.assertEqual(knownPairs, pairList)

    def test_canGetBaseCurrencies(self):
        cp = CurrencyPair()
        baseCurrs = cp.getBaseCurrencies()
        # currently defined are USD, EUR
        self.assertTrue('USD' in baseCurrs)
        self.assertTrue('EUR' in baseCurrs)
        self.assertFalse('CHF' in baseCurrs)


if __name__ == '__main__':
    unittest.main()
