from financial_statement import financial_statement

class balance_sheet(financial_statement):
  def __init__(self, co, periodicity, timestamp):
    financial_statement.__init__(self, co, periodicity, timestamp)
    self.statement = 'Balance Sheet'
    self.retained_earnings = None
    self.share_capital = None

  def __call__(self, retained_earnings):
    self.retained_earnings = retained_earnings
    self.share_capital = self.co.accounts['Equity']['Share Capital']()
    self.total_equity = self.retained_earnings + self.share_capital
    return self.total_equity

  def __repr__(self):
    header = financial_statement.__repr__(self)
    assets = 'Assets\n'
    for key, value in self.co.accounts['Assets'].items():
      assets += '{:20} {:>10}\n'.format(key, accounting_print(value()))
    total_assets = sum([self.co.accounts['Assets'][k]() for k in self.co.accounts['Assets'].keys()])
    assets += 'TOTAL Assets {:>25}\n\n'.format(accounting_print(total_assets))
    liabilities = 'Liabilities\n'
    for key, value in self.co.accounts['Liabilities'].items():
      liabilities += '{:20} {:>10}\n'.format(key, accounting_print(value()))
    total_liabilities = sum([self.co.accounts['Liabilities'][k]() for k in self.co.accounts['Liabilities'].keys()])
    liabilities += 'TOTAL Liabilities {:>20}\n\n'.format(accounting_print(total_liabilities))
    equity = 'Equity\n'
    equity += '{:20} {:>10}\n'.format('Share Capital', self.share_capital)
    equity += '{:20} {:>10}\n'.format('Retained Earnings', accounting_print(self.retained_earnings))
    equity += 'TOTAL Equity {:>25}\n'.format(self.total_equity)
    #assert total_assets == (total_liabilities + self.total_equity), "Does not balance"
    return header + assets + liabilities + equity


if __name__ == '__main__':
  from datetime import datetime
  
