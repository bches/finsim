class InsufficientFundsError(Exception):
    pass


class account:
    def __init__(self):
        self.zero()
        
    def __repr__(self):
        return '{:{prec}}|{:{prec}}\n'.format(sum(self._dr),
                                              sum(self._cr),
                                              prec=10)

    def debit(self, amount):
        assert amount >= 0, "Debit amount must be >= 0"
        self._dr += [amount]

    def credit(self, amount):
        assert amount >= 0, "Credit amount must be >= 0"
        self._cr += [amount]

    def zero(self):
        self._cr = [0]
        self._dr = [0]
    

class asset_account(account):
    def net(self):
        return sum(self._dr) - sum(self._cr)

    def increase(self, amount):
        self.debit(amount)

    def decrease(self, amount):
        self.credit(amount)

    def balance(self):
        return self.net(), 0


class cash_account(asset_account):
    def __init__(self):
        asset_account.__init__(self)
    
    def credit(self, amount):
        assert amount >= 0, "Credit amount must be >= 0"
        if amount > self.net():
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
        return 0, self.net()


class equity_account(liabilities_account):
    pass



if __name__ == '__main__':
    cash = asset_account()
    cash.debit(2700)
    print(cash)
    print()
    print('cash() =', cash.net())
    print()
    print('balance:', cash.balance())
    assert cash.net() == 2700, 'Cash not debited correctly'

    cash = cash_account()
    cash.debit(2000)
    print(cash)
    print()
    print('cash() =', cash.net())
    print()
    print('balance:', cash.balance())
    try:
        cash.credit(2700)
    except InsufficientFundsError:
        print('Correctly caught overdraft')
