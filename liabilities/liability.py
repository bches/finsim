from ..accounting.account import account
from datetime import datetime

class liability(account):
    def __add__(self, other):
        assert isinstance(other, asset), "Must add asset to another asset"
        return self.net() + other.net()

    def net(self):
        return sum(self._cr) - sum(self._dr)

    def increase(self, amount):
        self.credit(amount)

    def decrease(self, amount):
        self.debit(amount)

    def balance(self):
        return 0, self()

    def pay(self, _to, amount):
        assert amount <= self.net(), "Payment amount must be <= net()"
        self.decrease(amount)
        # create an expense
        # return expense(amount)
    

class tax_liability(liability):
    def __init__(self, taxing_entity, label, code, activity=None, tax_rate=None):
        self.taxing_entity = taxing_entity
        liability.__init__(self, label, code, activity=None)
        self.tax_rate = tax_rate
        
    def __repr__(self):
        s = '<Instance of %s at %s:\n' % (self.__class__.__name__, id(self))
        s += 'taxing_entity = %s,\n' % self.taxing_entity
        s += 'tax_rate = %s,\n' % self.tax_rate
        return s + account.__repr__(self)

    def set_tax_rate(self, rate):
        self.tax_rate = rate

    def pay(self, amount):
        return liability.pay(self, _to=self.taxing_entity, amount=amount)
        
        
class s1231(tax_liability):
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
    pass
