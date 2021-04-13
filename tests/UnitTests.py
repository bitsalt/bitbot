import unittest
import configparser

from oanda_backtest import Backtest
import oandapyV20 as opy
import pandas as pd
import v20

import Forex.config as fxconfig
from Forex.Account import Account
from Forex.Currency import Currency
from Forex.CurrencyPair import CurrencyPair
from Forex.Pricing import Pricing


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

    def test_canMakeConfigInstance(self):
        cfg = fxconfig.make_config_instance()
        self.assertIsInstance(cfg, fxconfig.Config)

    def test_canGetAccountIdFromConfig(self):
        cfg = fxconfig.make_config_instance()
        acct = cfg.active_account
        self.assertEqual('101-001-18641898-0001', acct)

    def test_canCreateContext(self):
        cfg = fxconfig.make_config_instance()
        api = cfg.create_context()
        self.assertIsInstance(api, v20.Context)

    def test_canGetAccountInfoFromAPI(self):
        cfg = fxconfig.make_config_instance()
        api = cfg.create_context()
        response = api.account.summary(cfg.active_account)
        self.assertEqual(200, response.status)

        account = response.body['account']
        self.assertEqual('USD', account.currency)

    def test_canGetAccountInfoFromAccountClass(self):
        acct = Account()
        # curr = acct.get_account_info('currency')
        self.assertEqual('USD', acct.currency)
        self.assertEqual('Primary', acct.alias)

    def test_canGetPriceQuote(self):
        quote = Pricing()
        price = quote.get_price('USD_CAD')

        self.assertGreater(1.4000, price.bid)
        self.assertGreater(price.ask, price.bid)
        # assertAlmostEqual should pass most of the time, but might fail on occasion
        self.assertAlmostEqual(price.bid, price.ask, 3)

    # def test_canGetAccountDataWithAlternateAPIWrapper(self):
    #     config = configparser.ConfigParser()
    #     config.read('../oanda.cfg')
    #     api = opy.API(
    #         environment='practice',
    #         access_token=config['oanda']['access_token']
    #     )
    #
    #     data = api.get_history(
    #         instrument='EUR_USD',
    #         start='2021-04-01',
    #         end='2021-04-13',
    #         granularity='H1'
    #     )
    #     df = pd.DataFrame(data['candles']).set_index('time')
    #     df.index = pd.DatetimeIndex(df.index)
    #     df.info()
    #     self.assertTrue(api)

    def test_canBacktestOanda(self):
        config = configparser.ConfigParser()
        config.read('../oanda.cfg')
        #     api = opy.API(
        #         environment='practice',
        #         access_token=config['oanda']['access_token']
        bt = Backtest(
            access_token=config['oanda']['access_token'],
            environment='practice'
        )
        params = {
            "granularity": "H1",  # 1 hour candlesticks (default=S5)
            "count": 5000  # 5000 candlesticks (default=500, maximum=5000)
        }
        bt.candles('USD_CAD', params)

        fast_ma = bt.ema(period=12)
        slow_ma = bt.ema(period=30)
        exit_ma = bt.ema(period=5)

        bt.buy_entry = (fast_ma > slow_ma) & (fast_ma.shift() <= slow_ma.shift())
        bt.sell_entry = (fast_ma < slow_ma) & (fast_ma.shift() >= slow_ma.shift())
        bt.buy_exit = (bt.C < exit_ma) & (bt.C.shift() >= exit_ma.shift())
        bt.sell_exit = (bt.C > exit_ma) & (bt.C.shift() <= exit_ma.shift())

        bt.initial_deposit = 1000  # default=0
        bt.units = 15000  # currency unit (default=10000)
        bt.stop_loss = 50  # stop loss pips (default=0)
        bt.take_profit = 75
        bt.run()
        bt.plot()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
