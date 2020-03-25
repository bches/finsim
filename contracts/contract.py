class contract:
    '''A contract is a virtual base class for financial agreements
    between companies or individuals'''
    def __init__(self, payee, payer, amount):
        assert 'Cash' in payee, 'Payee needs a Cash account'
        assert 'Cash' in payer, 'Payer needs a Cash account'
        assert 'Accounts Receivable' in payee, 'Payee needs an Accounts Receivable account'
        assert 'Accounts Payable' in payer, 'Payer needs an Accounts Payable account'
        self.payee = payee
        self.payer = payer
        self.balance = amount
        self.payer['Accounts Payable'].increase(amount)
        self.payee['Accounts Receivable'].increase(amount)

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
        self.payer['Cash'].decrease(amount)
        self.payer['Accounts Payable'].decrease(amount)
        self.payee['Cash'].increase(amount)
        self.payee['Accounts Receivable'].decrease(amount)
        self.balance -= amount


if __name__ == '__main__':
    from ..accounting.service_provider import service_provider

    me = service_provider(name='My Company')
    print('me =', me)

    you = service_provider(name='Your Comoany')
    you['Cash'].increase(6)
    print('you =', you)

    print()

    dut = contract(payee=me, payer=you, amount=12)
    print(dut)
    print()

    dut.pay(5)
    print(dut)
    print()
