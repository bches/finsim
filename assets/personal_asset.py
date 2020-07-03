from ..assets.capital_asset import capital_gain
from ..assets.asset import asset
from datetime import timedelta


class personal_asset(asset):
    def sell(self, _to, selling_price):
        holding_period, gain = asset.sell(self, _to, selling_price)
        if holding_period > timedelta(days=365):
            return s1231(amount=gain, from_asset=self,
                         holding_period=holding_period)
        else:
            return ordinary_gain(amount=gain, from_asset=self,
                                 holding_period=holding_period)


class ordinary_gain(capital_gain):
    pass

    
class s1231(capital_gain):
    def __init__(self, amount, from_asset, holding_period):
        assert holding_period > timedelta(days=365), "Holding period must be longer than a year from section 1231 treatment"
        capital_gain.__init__(amount, from_asset, holding_period)


class s1245:
    def __init__(self):
        pass

    def __repr__(self):
        return
    
    def recapture(self):
        pass

    
class s1250:
    def recapture(self):
        pass

    def unrecapture(self):
        pass


