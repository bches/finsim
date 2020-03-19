from financial_statement import financial_statement

class statement_of_shareholders_equity(financial_statement):
    def __init__(self, co, periodicity, timestamp):
        financial_statement.__init__(self, co, periodicity, timestamp)
        self.statement = 'Statement of Shareholders Equity'
        self.opening_balance = {}
        self.ending_balance = {}
        self.net_income = None
        self.shares_issued = {}
        self.dividends = {}

    def __call__(self, net_income, previous_statement=None):
        self.net_income = net_income
        if previous_statement == None:
            self.opening_balance = {'Share Capital':0, 'Retained Earnings':0, 'Total Equity':0}
        else:
            assert type(previous_statement) is type(self), "Previous statement must be %s" % type(self)
        for each in ['Share Capital', 'Retained Earnings', 'Total Equity']:
            self.opening_balance[each] = previous_statement[each]
        self.ending_balance['Share Capital'] = self.co.accounts['Equity']['Share Capital']()
        self.share_capital_raised = self.ending_balance['Share Capital'] - self.opening_balance['Share Capital']
        self.dividends = self.co.accounts['Equity']['Dividends']()
        self.ending_balance['Retained Earnings'] = self.opening_balance['Retained Earnings'] + self.net_income + self.dividends
        self.ending_balance['Total Equity'] = self.opening_balance['Total Equity'] + self.share_capital_raised + self.net_income + self.dividends
        return self.ending_balance['Retained Earnings']

    def __getitem__(self, i):
        return self.ending_balance[i]

    def __repr__(self):
        header = financial_statement.__repr__(self)
        col1 = '{:20}{:15}{:15}{:15}\n'.format("", "Share", "Retained", "Total")
        col2 = '{:20}{:15}{:15}{:15}\n'.format("", "Capital", "Earnings", "Equity")
        opening_balance_str = '{:20}{:7}{:16}{:15}\n'.format("Opening Balance",
                                                             self.opening_balance['Share Capital'],
                                                             self.opening_balance['Retained Earnings'],
                                                             self.opening_balance['Total Equity'])
        shares_issued_str = '{:20}{:7}{:16}{:15}\n'.format("Shares Issued",
                                                           self.share_capital_raised, '',
                                                           self.share_capital_raised)
        net_income_str = '{:20}{:7}{:16}{:15}\n'.format("Net Income", '', 
                                                        self.net_income, self.net_income)
        dividends_str = '{:20}{:7}{:16}{:15}\n'.format("Dividends", '', 
                                                       self.dividends, self.dividends)
        ending_balance_str = '{:20}{:7}{:16}{:15}\n'.format("Ending Balance",
                                                            self.ending_balance['Share Capital'],
                                                            self.ending_balance['Retained Earnings'],
                                                            self.ending_balance['Total Equity'])
        return header + col1 + col2 + opening_balance_str + shares_issued_str + net_income_str + dividends_str + ending_balance_str


if __name__ == '__main__':
    from datetime import datetime
    from ..examples.big_dog_carworks import BigDog
    
    eq_stmt = statement_of_shareholders_equity(BigDog, 'Monthly',
                                               datetime(2001, 2, 3, 4, 5))
    eq_stmt(net_income=2057)
    print(eq_stmt)
