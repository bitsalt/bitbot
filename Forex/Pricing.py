import Forex.config as fxconfig
import time


class Pricing:

    def __init__(self):
        cfg = fxconfig.make_config_instance()
        self.account_id = cfg.active_account
        self.__api = cfg.create_context()
        self.latest_price_time = None
        self.latest_price = {}

    def get_price(self, currency_pair, stream=False, interval=10):
        if not stream:
            latest_price_time = self.poll(currency_pair, self.latest_price_time)
            return Price(self.latest_price)

        while stream:
            time.sleep(interval)
            self.latest_price_time = self.poll(self.latest_price_time)
            return Price(self.latest_price)



    def price_to_string(self):
        return "{} ({}) Bid:{} Ask:{}".format(
            self.latest_price.instrument,
            self.latest_price.time,
            self.latest_price.bids[0].price,
            self.latest_price.asks[0].price
        )

    def poll(self, currency_pair, latest_price_time=None):
        # response = self.__api.pricing.stream(self.account_id)

        response = self.__api.pricing.get(
            self.account_id,
            instruments=currency_pair,
            since=latest_price_time,
            includeUnitsAvailable=False
        )

        for price in response.get("prices", 200):
            if latest_price_time is None or price.time > latest_price_time:
                self.latest_price = price

        #
        # Stash and return the current latest price time
        #
        for price in response.get("prices", 200):
            if latest_price_time is None or price.time > latest_price_time:
                latest_price_time = price.time

        return latest_price_time

class Price:
    def __init__(self, price):
        self.instrument = price.instrument
        self.time = price.time
        self.bid = price.bids[0].price
        self.ask = price.asks[0].price