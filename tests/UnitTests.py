import unittest
from Forex.Currency import Currency
from Forex.CurrencyPair import CurrencyPair


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        self.currency = None

    def test_canCreateCurrency(self):
        self.currency = Currency('USD')
        self.assertIsInstance(self.currency, Currency)
        self.assertEqual(self.currency.currency, 'USD')

    def test_canGetCurrencyPair(self):
        usd = Currency('USD')
        known_pairs = [
                'EUR_USD',
                'USD_CAD',
                'USD_CHF',
                'AUD_USD',
                'NZD_USD',
                'GBP_USD',
                'USD_JPY'
            ]
        pair_list = usd.getPairsList()
        self.assertEqual(known_pairs, pair_list)

    def test_canGetBaseCurrencies(self):
        cp = CurrencyPair()
        base_curr = cp.getBaseCurrencies()
        # currently defined are USD, EUR
        self.assertTrue('USD' in base_curr)
        self.assertTrue('EUR' in base_curr)
        self.assertFalse('CHF' in base_curr)


if __name__ == '__main__':
    unittest.main()
