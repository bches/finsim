from ..accounting.account import expenses_account
from ..accounting.account import liabilities_account
from ..accounting.account import asset_account
from ..accounting.account import cash_account


class tax_account:
    def __init__(self, tax_rate, taxing):
        assert tax_rate < 1, "Tax rate must be < 1"
        self.tax_rate = tax_rate
        self.taxing = taxing
        self.cash = cash_account(None)
        self.assets = asset_account('Tax Assets', None, None)
        self.tax_paid = expenses_account('Tax Paid', None, None)
        self.tax_owed = liabilities_account('Tax Owed', None, None)
        
    def __repr__(self):
        s = '%s %s:\n' % (self.__class__.__name__, self.tax_rate)
        s += str(self.cash)
        s += str(self.assets)
        s += str(self.tax_paid)
        s += str(self.tax_owed)
        return s

    def incur_tax(self, gross_amount):
        assert gross_amount > 0, "Gross amount must be > 0"
        tax_amount = self.tax_rate * gross_amount
        net_amount = gross_amount - tax_amount
        self.tax_owed.increase(tax_amount)
        self.cash.increase(gross_amount)
    
    def pay_tax(self, amount):
        assert amount > 0, "Amount must be > 0"
        self.tax_owed.decrease(amount)
        self.tax_paid.increase(amount)
        self.cash.decrease(amount)
        self.taxing.pay(amount)


if __name__ == '__main__':
    from ..taxes.taxing_entity import taxing_entity

    state = taxing_entity()
    
    sales_tax = tax_account(tax_rate=0.05,
                            taxing=state)
    
    after_tax = sales_tax.incur_tax(gross_amount=1000)

    sales_tax.pay_tax(amount=40)
    print('sales_tax=',sales_tax)
    print('state=',state)
    
