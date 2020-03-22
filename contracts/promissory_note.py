from ..contracts.bad_debt import bad_debt


class promissory_note(bad_debt):
    '''A promissory note is a short-term loan (less than a year)'''
    def __init__(self, payee, payer, amount, interest_rate, term):
        bad_debt.__init__(self, payee, payer, amount)
        assert 'Interest Receivable' in self.payee, 'Payee needs an Interest Receivable account'
        assert 'Interest Revenue' in self.payee, 'Payee needs Interest Revenue account'
        assert 'Interest Payable' in self.payer, 'Payer needs an Interest Payable account'
        assert 'Interest Expense' in self.payer, 'Payer needs Interest Expense account'
        assert term > 1, 'Term must be greater than 1'
        self.interest_rate = interest_rate
        self.term = term
        r = interest_rate
        n = term
        self.payment = amount * r / (1 - 1 / ((1+r) ** n))
        self.total_interest = term * self.payment - amount
        self.payee['Interest Receivable'].increase(self.total_interest)
        self.payer['Interest Payable'].increase(self.total_interest)
        
    def __repr__(self):
        s = bad_debt.__repr__(self)
        interest_rate = self.interest_rate
        payment = self.payment
        term = self.term
        s += '\n\tinterest_rate = %s' % interest_rate
        s += '\n\tpayment = %s' % payment
        s += '\n\tterm = %s' % term
        return s

    def __iter__(self):
        for i in range(self.term):
            self.pay(min(self.payment, self.balance))
            interest = self.total_interest / self.term
            self.payee['Interest Receivable'].decrease(interest)
            self.payee['Interest Revenue'].increase(interest)
            self.payer['Interest Payable'].decrease(interest)
            self.payer['Interest Expense'].increase(interest)
            yield


if __name__ == '__main__':
    from ..accounting.portfolio import portfolio

    me = portfolio(name='My Company')
    me.add_revenue_category(name='Interest Revenue', code=560)
    me.add_asset_category(name='Interest Receivable', code=160)
    print('me =', me)
    
    you = portfolio(name='Your Comoany')
    you.add_expense_category(name='Interest Expense', code=660)
    you.add_liability_category(name='Interest Payable', code=220)
    
    print('you =', you)
    you['Cash'].increase(6000)
    
    print()

    dut = promissory_note(payee=me, payer=you,
                          amount=5000, interest_rate=0.01,
                          term=12)
    print(dut)
    print()

    for payment in dut:
        print('Paying...')
    
    print(dut)
    print()
    
