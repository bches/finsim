from ..contracts.loan import loan


class invoice(loan):
    '''An invoice can be converted to a loan if it goes unpaid
    so the invoice object inherits from the loan object'''
    def __init__(self, payee, payer, amount, interest_rate, term,
                 description=None):
        '''The creation of an invoice is a bid, and may not be
        accepted by the payer'''
        loan.__init__(self, payee, payer, amount, interest_rate, term)
        self.description = description
        self.accepted = False

    def __repr__(self):
        s = loan.__repr__(self)
        s += '\tdescription = %s' % self.description
        s += '\taccepted = %s' % self.accepted

    def accept(self):
        self.accepted = True
        self.payee['Accounts Receivable'].increase(self.amount)
        self.payer['Accounts Payable'].increase(self.amount)
