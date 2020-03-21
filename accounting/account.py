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


if __name__ == '__main__':
    cash = asset_account('Cash', 101)
    cash.debit(2700)
    print(cash)
    print()
    print('cash() =', cash())
    print()
    print('balance:', cash.balance())
    assert cash() == 2700, 'Cash not debited correctly'
