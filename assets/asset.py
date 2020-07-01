from ..base.account import asset_account
from datetime import datetime


class asset(asset_account):
    def __init__(self, historical_cost=None, owner=None, date_acquired=None):
        asset_account.__init__(self)
        self.historical_cost = historical_cost
        self.owner = owner
        self.date_acquired = date_acquired

    def __repr__(self):
        s = '<Instance of %s at %s:\n' % (self.__class__.__name__, id(self))
        s += 'owner = %s,\n' % self.owner
        s += 'historical_cost = %s,\n' % self.historical_cost
        s += 'date_acquired = %s,\n' % self.date_acquired
        return s + asset_account.__repr__(self)
        
    def __add__(self, other):
        assert isinstance(other, asset), "Must add asset to another asset"
        return self.net() + other.net()
        
    def sell(self, _to, selling_price):
        assert _to != None, "Cannot sell to None"
        assert _to != self.owner, "Cannot sell to current owner"
        selling_date =  datetime.today()
        if self.date_acquired != None:
            holding_period = selling_date - self.date_acquired
        self.date_acquired = selling_date
        self.historical_cost = selling_price
        self.owner = _to        
        self.zero()
        self.debit(selling_price)
        # create a tax gain or loss
        # if holding_period < 1 year:
        #  return tax_liability(selling_price, historical_cost, accumulated_depreciation)
        # else:
        # return s1231(selling_price, historical_cost, accumulated_depreciation)

if __name__ == '__main__':
    dut = asset(historical_cost=500.0, owner='me', date_acquired=datetime.today())
    print(dut)
    print()
    print('Selling to you...')
    result = dut.sell(_to='you', selling_price=1000.0)
    print('dut=', dut)
    print
    print('sale resulted in:', result)
        
