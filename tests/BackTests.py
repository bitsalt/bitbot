import unittest
import configparser

from oanda_backtest import Backtest


class UnitTests(unittest.TestCase):

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

        # bt.candles('EUR_USD', params)
        # fast_ma = bt.ema(period=9)
        # slow_ma = bt.ema(period=30)
        # exit_ma = bt.ema(period=5)

        bt.buy_entry = (fast_ma > slow_ma) & (fast_ma.shift() <= slow_ma.shift())
        bt.sell_entry = (fast_ma < slow_ma) & (fast_ma.shift() >= slow_ma.shift())
        bt.buy_exit = (bt.C < exit_ma) & (bt.C.shift() >= exit_ma.shift())
        bt.sell_exit = (bt.C > exit_ma) & (bt.C.shift() <= exit_ma.shift())

        bt.initial_deposit = 1000  # default=0
        bt.units = 18000  # currency unit (default=10000)
        bt.stop_loss = 30  # stop loss pips (default=0)
        bt.take_profit = 80
        print(bt.run())
        bt.plot()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()


'''
Best runs...
bt.candles('USD_CAD', params)
        fast_ma = bt.ema(period=12)
        slow_ma = bt.ema(period=30)
        exit_ma = bt.ema(period=5)
'''