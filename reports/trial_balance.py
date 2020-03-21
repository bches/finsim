from math import fabs
from ..utils import accounting_print
from ..reports.financial_statement import financial_statement


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
