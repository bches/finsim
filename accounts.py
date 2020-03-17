from datetime import datetime
from math import fabs

class account:
  def __init__(self, label, code, activity=None):
    self.label = label
    self.code = code
    self.activity = activity
    self._cr = [0]
    self._dr = [0]   

  def __repr__(self):
    return '{:>{width}} : {}\n{}\n{:{prec}}|{:{prec}}\n'.format(self.label,
                                                 self.code, '-'*21,
                                                 sum(self._dr),
                                                 sum(self._cr),
                                                 width=10,prec=10)
    
  def debit(self, amount):
    assert amount >= 0, "Debit amount must be >= 0"
    self._dr += [amount]

  def credit(self, amount):
    assert amount >= 0, "Credit amount must be >= 0"
    self._cr += [amount]

class asset_account(account):
  def __call__(self):
    return sum(self._dr) - sum(self._cr)

  def increase(self, amount):
    self.debit(amount)

  def decrease(self, amount):
    self.credit(amount)

  def balance(self):
    return self(), 0

class dividends_account(asset_account):
  pass

class expenses_account(asset_account):
  pass

class liabilities_account(account):
  def __call__(self):
    return sum(self._cr) - sum(self._dr)

  def increase(self, amount):
    self.credit(amount)

  def decrease(self, amount):
    self.debit(amount)

  def balance(self):
    return 0, self()

class equity_account(liabilities_account):
  pass

def accounting_print(x):
  if x < 0: return f'({-1*x})'
  if x > 0: return f'{x}'
  return ''
  
  
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
    s = '{:20}{:>10}{:>10}\n{:20}{:>10}\n     {:20}{:>15}\n{}'.format(self.__class__.__name__,'Dr','Cr',
                                  self.debit_account.label, self.amount,
                                  self.credit_account.label, self.amount,
                                  self.description)
    return s


class PortfolioAccountError(Exception):
  pass

class portfolio:
  def __init__(self, name):
    self.name = name
    self.accounts = {'Assets':{}, 'Liabilities':{}, 'Equity':{}, 
                     'Revenues':{}, 'Expenses':{}}
    self.all_codes = set({})
    self.add_asset_category(name='Cash', code=101)
    self.add_asset_category(name='Accounts Receivable', code=110)
    self.add_liability_category(name='Accounts Payable', code=210)

  def __repr__(self):
    s = '<%s %s :\n' % (self.__class__.__name__, self.name)
    for each in self:
        s += '%s\n' % each
    s += '>'
    return s

  def __getitem__(self, i):
    for acct in self:
      if type(i) is type(str()):
        if acct.label == i: return acct
      if type(i) is type(int()):
        if acct.code == i: return acct
    raise CompanyAccountError('Account %s not found in %s' % (i, self.__class__.__name__))

  def __iter__(self):
    for acct_type in self.accounts.keys():
      for acct in self.accounts[acct_type].keys():
        yield self.accounts[acct_type][acct]

  def add_revenue_category(self, name, code):
    assert name not in self.accounts['Revenues'].keys(), "That revenue account already exists"
    assert code not in self.all_codes, "That code is already being used"
    self.accounts['Revenues'][name] = equity_account(name, code, activity='Operating')
    self.all_codes.add(code)

  def add_expense_category(self, name, code):
    assert name not in self.accounts['Expenses'].keys(), "That expense account already exists"
    assert code not in self.all_codes, "That code is already being used"
    self.accounts['Expenses'][name] = expenses_account(name, code, activity='Operating')
    self.all_codes.add(code)

  def add_asset_category(self, name, code, activity=None):
    assert name not in self.accounts['Assets'].keys(), "That asset account already exists"
    assert code not in self.all_codes, "That code is already being used"
    self.accounts['Assets'][name] = asset_account(name, code, activity)
    self.all_codes.add(code)

  def add_liability_category(self, name, code, activity=None):
    assert name not in self.accounts['Liabilities'].keys(), "That liability account already exists"
    assert code not in self.all_codes, "That code is already being used"
    self.accounts['Liabilities'][name] = liabilities_account(name, code, activity)
    self.all_codes.add(code)

  def add_equity(self):
    self.accounts['Equity']['Share Capital'] = equity_account('Share Capital', 320, activity='Financing')
    self.accounts['Equity']['Dividends'] = dividends_account('Dividends', 330, activity='Financing')
    self.all_codes.update({320, 330})

  def allocate_share_capital(self, amount):
    self.accounts['Assets']['Cash'].increase(amount)
    self.accounts['Equity']['Share Capital'].increase(amount)

  def allocate_dividends(self, amount):
    self.accounts['Assets']['Cash'].decrease(amount)
    self.accounts['Equity']['Dividends'].decrease(amount)

  def borrow(self, liability, amount):
    self.accounts['Assets']['Cash'].increase(amount)
    self.accounts['Liabilities'][liability].increase(amount)

  def purchase_asset(self, asset, amount):
    self.accounts['Assets']['Cash'].decrease(amount)
    self.accounts['Assets'][asset].increase(amount)

  def finance_asset(self, asset, price, liability, amount_financed):
    assert price >= amount_financed, "Cannot finance for more than the price."
    self.accounts['Assets'][asset].increase(price)
    self.accounts['Assets']['Cash'].decrease(price - amount_financed)
    self.accounts['Liabilities'][liability].increase(amount_financed)

  def pay_liability(self, liability, amount):
    self.accounts['Assets']['Cash'].decrease(amount)
    self.accounts['Liabilities'][liability].decrease(amount)

  def receive_payment(self, revenue, amount, total=None):
    self.accounts['Assets']['Cash'].increase(amount)
    if total == None: total = amonunt
    if total > amount:
      self.accounts['Assets']['Accounts Receivable'].increase(total-amount)
    self.accounts['Revenues'][revenue].increase(total)

  def pay_expense(self, expense, amount):
    self.accounts['Assets']['Cash'].decrease(amount)
    # Expenses is a contra account to equity, which decreases with Cash decreasing,
    # so Expenses ends up increasing
    self.accounts['Expenses'][expense].increase(amount)

  def borrow_expense(self, expense, amount):
    self.accounts['Liabilities']['Accounts Payable'].increase(amount)
    # Expenses is a contra account to equity, which decreases with Cash decreasing,
    # so Expenses ends up increasing
    self.accounts['Expenses'][expense].increase(amount)

  def adjust_prepaid_asset(self, asset, expense, amount, description):
    '''Debit an expense to adjust a prepaid asset for the amount used'''
    adj = adjusting_entry(debit_account=self.accounts['Expenses'][expense],
                          credit_account=self.accounts['Assets'][asset])
    adj(amount, description)
    return adj

  def adjust_depreciate_ppe(self, asset, amount, description):
    '''Debit depreciation expense and credit accumulated depreciation for plant,
    property and equipment'''
    adj = adjusting_entry(debit_account=self.accounts['Expenses']['%s Dep.' % asset],
                          credit_account=self.accounts['Liabilities']['Acc. %s Dep.' % asset])
    adj(amount, description)
    return adj

  def adjust_accrued_expenses(self, expense, amount, description):
    '''Accrue an expense, such as interest on a loan'''
    adj = adjusting_entry(debit_account=self.accounts['Expenses']['%s Expense' % expense],
                          credit_account=self.accounts['Liabilities']['%s Payable' % expense])
    adj(amount, description)
    return adj

  def adjust_unearned_liabilities(self, revenue, amount, description):
    '''Adjust an unearned liability for the amount earned'''
    adj = adjusting_entry(debit_account=self.accounts['Liabilities']['Unearned Revenue'],
                          credit_account=self.accounts['Revenues']['%s Revenues' % revenue])
    adj(amount, description)
    return adj

  def adjust_unearned_revenue(self, revenue, amount, description):
    '''Earn revenue'''
    adj = adjusting_entry(debit_account=self.accounts['Liabilities']['Unearned Revenue'],
                          credit_account=self.accounts['Revenues']['%s Revenues' % revenue])
    adj(amount, description)
    return adj

  def adjust_accrued_revenue(self, revenue, amount, description):
    '''Accrue revenue'''
    adj = adjusting_entry(debit_account=self.accounts['Assets']['Accounts Receivable'],
                          credit_account=self.accounts['Revenues']['%s Revenues' % revenue])
    adj(amount, description)
    return adj


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
    lines = '{:^5} {:20} {:>10} {:>10}\n'.format('No.', 'Account', 'Dr.', 'Cr.')
    total = {'dr':0, 'cr':0}
    for code in codes:
      acct = self.co[code]
      (dr, cr) = map(int, map(fabs, acct.balance()))
      total['dr'] += dr
      total['cr'] += cr
      lines += '{:^5} {:20} {:>10} {:>10}\n'.format(code, acct.label, 
                                                    accounting_print(dr), 
                                                    accounting_print(cr))
    total_str = '{:^5} {:20} {:>10} {:>10}\n'.format('','', total['dr'], 
                                                     total['cr'])
    assert total['dr'] == total['cr'], "Does not balance."
    return header + lines + total_str


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
                                                       self.share_capital_raised,
                                                       '',
                                                       self.share_capital_raised)
    net_income_str = '{:20}{:7}{:16}{:15}\n'.format("Net Income",
                                                    '', self.net_income, self.net_income)
    dividends_str = '{:20}{:7}{:16}{:15}\n'.format("Dividends",
                                                    '', self.dividends, 
                                                   self.dividends)
    ending_balance_str = '{:20}{:7}{:16}{:15}\n'.format("Ending Balance",
                                                          self.ending_balance['Share Capital'],
                                                          self.ending_balance['Retained Earnings'],
                                                          self.ending_balance['Total Equity'])
    return header + col1 + col2 + opening_balance_str + shares_issued_str + net_income_str + dividends_str + ending_balance_str


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


