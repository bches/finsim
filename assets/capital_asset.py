from ..assets.asset import asset
from datetime import timedelta


class capital_gain:
    def __init__(self, amount, from_asset, holding_period):
        assert amount >= 0, 'Amount must be >= 0.'
        self.amount = amount
        self.from_asset = from_asset
        self.holding_period = holding_period

    def __repr__(self):
        s = '<Instance of %s at %s:\n' % (self.__class__.__name__, id(self))
        s += '\tfrom_asset = %s,\n' % self.from_asset
        s += '\tholding_period = %s,\n' % self.holding_period
        s += '\tgain = %d>' % self.amount
        return s

    def __add__(self, other):
        assert isinstance(self.__class__.__name__,
                          other), 'Must add capital_gain instance ot another capital_gain instance'
        return self.amount + other.amount
            

class capital_asset(asset):
    def sell(self, _to, selling_price):
        holding_period, gain = asset.sell(self, _to, selling_price)
        return capital_gain(amount=gain, from_asset=self,
                            holding_period=holding_period)


if __name__ == '__main__':
    from datetime import datetime
    
    a = capital_asset(historical_cost=1200.0, owner='me',
                      date_acquired=datetime(2007, 12, 3, 4, 5))

    print('a=',a)
    print()

    print('Selling to you...')
    result = a.sell(_to='you', selling_price=1900)
    print('a=',a)
    print()
    print('result=',result)
