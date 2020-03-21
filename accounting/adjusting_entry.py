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
        s = '{:20}{:>10}{:>10}\n\
        {:20}{:>10}\n     {:20}{:>15}\n{}'.format(self.__class__.__name__,
                                                  'Dr', 'Cr',
                                                  self.debit_account.label,
                                                  self.amount,
                                                  self.credit_account.label,
                                                  self.amount,
                                                  self.description)
        return s
