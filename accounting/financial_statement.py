from math import fabs
from ..accounting.account import accounting_print


class financial_statement:
    def __init__(self, co, periodicity, timestamp):
        self.co = co
        self.statement = 'Financial Statement'
        self.ending = 'For the %s Ending %s' % (periodicity, timestamp.ctime())

    def __repr__(self):
        company = self.co.name
        statement = self.statement
        ending = self.ending
        return f'{company}\n\
{statement}\n\
{ending}\n\n'


class trial_balance(financial_statement):
    def __init__(self, co, periodicity, timestamp):
        financial_statement.__init__(self, co, periodicity, timestamp)
        self.statement = 'Trial Balance'

    def __call__(self):
        pass

    def __repr__(self):
        header = financial_statement.__repr__(self)
        codes = list(self.co.all_codes)
        codes.sort()
        lines = '{:^5} {:20} {:>10} {:>10}\n'.format('No.', 'Account',
                                                     'Dr.', 'Cr.')
        total = {'dr': 0, 'cr': 0}
        for code in codes:
            acct = self.co[code]
            (dr, cr) = map(int, map(fabs, acct.balance()))
            total['dr'] += dr
            total['cr'] += cr
            lines += '{:^5} {:20} {:>10} {:>10}\n'.format(code, acct.label,
                                                          accounting_print(dr),
                                                          accounting_print(cr))
        total_str = '{:^5} {:20} {:>10} {:>10}\n'.format('', '', total['dr'],
                                                         total['cr'])
        assert total['dr'] == total['cr'], "Does not balance."
        return header + lines + total_str


if __name__ == '__main__':
    from datetime import datetime
    from ..examples.big_dog_carworks import BigDog

    adjusted = trial_balance(co=BigDog, periodicity='Monthly',
                             timestamp=datetime(2001, 2, 3, 4, 5))
    adjusted()
    print('Adjusted:')
    print(adjusted)
