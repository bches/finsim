from ..assets.asset import asset
from datetime import timedelta


class capital_gain:
    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        s = '<Instance of %s at %s:\n' % (self.__class__.__name__, id(self))
        if self.amount < 0:
            s += '\tamount = (%d) [LOSS]' % (-self.amount)
        else:
            s += '\tamount = %d [GAIN]>' % self.amount
        return s

    def __add__(self, other):
        assert isinstance(self.__class__.__name__, other), 'Instances must be of the same type to add them'
        return capital_gain(self.amount + other.amount)

    def tax(self, rate):
        if self.amount <= 0: return 0
        return self.amount * rate
    
    
class capital_asset(asset):
    def sell(self, _to, selling_price):
        holding_period, gain = asset.sell(self, _to, selling_price)
        if holding_period > timedelta(days=365):
            print('holding period is long')
        else:
            print('holding period is short')
        return capital_gain(gain)


class s1231(capital_gain):
    pass


class s1245(s1231):
    def recapture(self):
        pass

    
class s1250(s1231):
    def recapture(self):
        pass

    def unrecapture(self):
        pass



if __name__ == '__main__':
    from datetime import datetime
    
    a = capital_asset(historical_cost=1200.0, owner='me',
                      date_acquired=datetime(2007, 12, 3, 4, 5))

    print('a=',a)
    print()

    print('Selling to you...')
    result = a.sell(_to='you', selling_price=900)
    print('a=',a)
    print()
    print('result=',result)
