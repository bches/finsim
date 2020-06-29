from ..accounting.account import account
from datetime import datetime


class asset(account):
    def __init__(self, label, code, activity=None):
        account.__init__(self, label, code, activity)
        self.historical_cost = None
        self.owner = None
        self.date_acquired = None

    def __repr__(self):
        s = '<Instance of %s at %s:\n' % (self.__class__.__name__, id(self))
        s += 'owner = %s,\n' % self.owner
        s += 'historical_cost = %s,\n' % self.historical_cost
        s += 'date_acquired = %s,\n' % self.date_acquired
        return s + account.__repr__(self)
        
    def __add__(self, other):
        assert isinstance(other, asset), "Must add asset to another asset"
        return self.net() + other.net()
        
    def net(self):
        return sum(self._dr) - sum(self._cr)

    def increase(self, amount):
        self.debit(amount)

    def decrease(self, amount):
        self.credit(amount)

    def balance(self):
        return self(), 0

    def sell(self, _to, amount):
        self.historical_cost = amount
        self.owner = _to
        self.date_acquired = datetime.today()
        

        
if __name__ == '__main__':
    dut = asset(label='test', code=999)
    dut.sell(_to='me', amount=1000.0)
    print(dut)
        
