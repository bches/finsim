class contract:
    '''A contract is a virtual base class for financial agreements
    between companies or individuals'''
    def __init__(self, payee, payer, amount):
        self.payee = payee
        self.payer = payer
        self.balance = amount

    def __repr__(self):
        cls = self.__class__.__name__
        payee = self.payee
        payer = self.payer
        balance = self.balance
        return f'<{cls} between {payee} and {payer}>:\n\
\tbalance = {balance}'

    def pay(self, amount):
        assert amount > 0, "Must pay amount > 0."
        assert amount <= self.balance, "Cannot pay more than the balance"
        self.balance -= amount


if __name__ == '__main__':
    dut = contract(payee='me', payer='you', amount=12)
    print(dut)
    print()
    dut.pay(5)
    print(dut)
