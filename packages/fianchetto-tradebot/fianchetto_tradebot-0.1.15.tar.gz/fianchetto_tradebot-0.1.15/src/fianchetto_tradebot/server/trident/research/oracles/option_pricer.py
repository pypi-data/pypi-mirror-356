import datetime

from fianchetto_tradebot.common_models.finance.amount import Amount
from fianchetto_tradebot.common_models.finance.option import Option


class OptionPricer:
    def __init__(self, interest_rate):
        self.interest_rate = interest_rate

    def estimate_option_price_given(self, option: Option, at_time: datetime.datetime, at_price: Amount, at_interest_rate=None):

        pass