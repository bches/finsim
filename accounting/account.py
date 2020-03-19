class account:
    def __init__(self, label, code, activity=None):
        self.label = label
        self.code = code
        self.activity = activity
        self._cr = [0]
        self._dr = [0]   

    def __repr__(self):
        return '{:>{width}} : {}\n{}\n{:{prec}}|{:{prec}}\n'.format(self.label,
                                                                    self.code, '-'*21,
                                                                    sum(self._dr),
                                                                    sum(self._cr),
                                                                    width=10,prec=10)

    def debit(self, amount):
        assert amount >= 0, "Debit amount must be >= 0"
        self._dr += [amount]

    def credit(self, amount):
        assert amount >= 0, "Credit amount must be >= 0"
        self._cr += [amount]

class asset_account(account):
    def __call__(self):
        return sum(self._dr) - sum(self._cr)

    def increase(self, amount):
        self.debit(amount)

    def decrease(self, amount):
        self.credit(amount)

    def balance(self):
        return self(), 0

class dividends_account(asset_account):
    pass

class expenses_account(asset_account):
    pass

class liabilities_account(account):
    def __call__(self):
        return sum(self._cr) - sum(self._dr)

    def increase(self, amount):
        self.credit(amount)

    def decrease(self, amount):
        self.debit(amount)

    def balance(self):
        return 0, self()

class equity_account(liabilities_account):
    pass

def accounting_print(x):
    if x < 0: return f'({-1*x})'
    if x > 0: return f'{x}'
    return ''
  
  
class adjusting_entry:
    def __init__(self, debit_account, credit_account):
        self.debit_account = debit_account
        self.credit_account = credit_account
        self.amount = 0
        self.description = ''

    def __call__(self, amount, description):
        self.amount = amount
        self.description = description
        self.debit_account.debit(amount)
        self.credit_account.credit(amount)

    def __repr__(self):
        s = '{:20}{:>10}{:>10}\n{:20}{:>10}\n     {:20}{:>15}\n{}'.format(self.__class__.__name__,
                                                                          'Dr','Cr',
                                                                          self.debit_account.label, 
                                                                          self.amount,
                                                                          self.credit_account.label, 
                                                                          self.amount,
                                                                          self.description)
        return s

  
if __name__ == '__main__':
    cash = asset_account('Cash', 101)
    cash.debit(2700)
    print(cash)
    print()
    print('balance:', cash.balance())
    assert cash() < 0, 'Cash not debited correctly'
