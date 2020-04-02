class InsufficientFundsError(Exception):
    pass

class MetaAccountError(Exception):
    pass


class account:
    def __init__(self, label, code, activity=None):
        self.label = label
        self.code = code
        self.activity = activity
        self._cr = [0]
        self._dr = [0]

    def __repr__(self):
        return '{:>{width}} : {}\n\
        {}\n{:{prec}}|{:{prec}}\n'.format(self.label,
                                          self.code, '-'*21,
                                          sum(self._dr),
                                          sum(self._cr),
                                          width=10, prec=10)

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


class cash_account(asset_account):
    def __init__(self, code):
        asset_account.__init__(self, label='Cash', code=code)
    
    def credit(self, amount):
        assert amount >= 0, "Credit amount must be >= 0"
        if amount > self():
            raise InsufficientFundsError('Insufficient Funds at %s')
        self._cr += [amount]


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


class meta_account(account):
    def __init__(self, name, code, activity=None):
        self.label = label
        self.code = code
        self.activity = activity
        self.subaccounts = {}

    def __repr__(self):
        return '{:>{width}} : {}\n\
        {}\n{}\n'.format(self.label,
                         self.code, '-'*21,
                         self.subaccounts)

    def __call__(self):
        return sum([acct() for acct in self.subaccounts])

    def add_subaccount(self, name):
        assert isinstance(name, account), "Must be an account"
        assert name not in self.subaccounts, "That subaccount already exists"
        self.subaccounts[name] = account(name=name,
                                         code=self.code,
                                         activity=self.activity)

    def remove_subaccount(self, name):
        assert name in self.subaccounts, "Account not found"
        assert self.subaccounts[name]() == 0, "Balance not 0"
        self.subaccount.remove(acct)

    def increase(self, name, amount):
        self.subaccounts[name].increase(amount)

    def decrease(self, name, amount):
        self.subaccounts[name].decrease(amount)

    def credit(self, name, amount):
        self.subaccounts[name].credit(amount)

    def debit(self, name, amount):
        self.subaccount[name].debit(amount)

    def subaccount_balance(self, name):
        assert name in self.subaccounts, "Not a subaccount"
        return self.subaccounts[name]()
    

if __name__ == '__main__':
    cash = asset_account('Cash', 101)
    cash.debit(2700)
    print(cash)
    print()
    print('cash() =', cash())
    print()
    print('balance:', cash.balance())
    assert cash() == 2700, 'Cash not debited correctly'

    cash = cash_account(code=101)
    cash.debit(2000)
    print(cash)
    print()
    print('cash() =', cash())
    print()
    print('balance:', cash.balance())
    try:
        cash.credit(2700)
    except InsufficientFundsError:
        print('Correctly caught overdraft')
