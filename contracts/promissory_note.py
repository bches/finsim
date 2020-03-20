import bad_debt

class promissory_note(bad_debt):
    '''A promissory note is a short-term loan (less than a year)'''
    def __init__(self, payee, payer, amount, interest_rate, term):
        contract.__init__(self, payee, payer, amount)
        assert 'Interest Receivable' in self.payee,
        'Payee needs an Interest Receivable account'
        assert 'Interest Revenue' in self.payee,
        'Payee needs Interest Revenue account'
        self.interest_rate = interest_rate
        self.term = term

    def __repr__(self):
        s = bad_debt.__repr__(self)
        interest_rate = self.interest_rate
        term = self.term
        s += '\n\tinterest_rate = {interest_rate}'
        s += '\n\tterm = {term}'
        return s

    def __iter__(self):
        for i in range(self.term):
            interest = self.interest_rate * self.balance
            payee['Interest Receivable'].debit(interest)
            payee['Interest Revenue'].credit(interest)
            self.balance += interest
            yield


if __name__ == '__main__':
    from ..examples.big_dog_carworks import BigDog
    
    dut = promissory_note(payee=BigDog, payer=None, amount=5000)
