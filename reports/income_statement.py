from ..reports.financial_statement import financial_statement
from ..utils import accounting_print

class income_statement(financial_statement):
    def __init__(self, co, periodicity, timestamp):
        financial_statement.__init__(self, co, periodicity, timestamp)
        self.statement = 'Income Statement'
        self.net_income = None

    def __repr__(self):
        header = financial_statement.__repr__(self)
        revenues = 'Revenues\n'
        for key, value in self.co.accounts['Revenues'].items():
            revenues += '   {:20} {:10}\n'.format(key, accounting_print(value()))
        total_revenues = sum([self.co.accounts['Revenues'][k]() for k in self.co.accounts['Revenues'].keys()])
        revenues += '     TOTAL Revenues {:>20}\n'.format(accounting_print(total_revenues))
        expenses = 'Expenses\n'
        for key, value in self.co.accounts['Expenses'].items():
            expenses += '   {:20} {:10}\n'.format(key, accounting_print(value()))
        total_expenses = sum([self.co.accounts['Expenses'][k]() for k in self.co.accounts['Expenses'].keys()])
        expenses += '     TOTAL Expenses {:>20}\n'.format(accounting_print(total_expenses))
        self.net_income = total_revenues - total_expenses
        net_inc = 'Net Income {:29}\n'.format(self.net_income)
        return header + revenues + expenses + net_inc

    def __call__(self):
        total_revenues = sum([self.co.accounts['Revenues'][k]() for k in self.co.accounts['Revenues'].keys()])
        total_expenses = sum([self.co.accounts['Expenses'][k]() for k in self.co.accounts['Expenses'].keys()])
        self.net_income = total_revenues + total_expenses
        return self.net_income


if __name__ == '__main__':
    from datetime import datetime
    from ..examples.big_dog_carworks import BigDog
    
    inc_stmt = income_statement(BigDog, 'Monthly', datetime(2001, 2, 3, 4, 5))
    print(inc_stmt)
