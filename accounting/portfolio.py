from ..accounting.account import account, asset_account, liabilities_account
from ..accounting.account import expenses_account, cash_account
from ..accounting.adjusting_entry import adjusting_entry


class PortfolioAccountError(Exception):
  pass

class portfolio:
  def __init__(self, name):
    self.name = name
    self.accounts = {'Assets':{}, 'Liabilities':{}, 'Expenses':{}}
    self.all_codes = set({})
    self.add_cash_account(code=101)
    self.add_liability_category(name='Accounts Payable', code=210)

  def __repr__(self):
    s = '<%s %s :\n' % (self.__class__.__name__, self.name)
    for each in self.accounts.keys():
        s += '%s\n' % self.accounts[each]
    s += '>'
    return s

  def __getitem__(self, i):
    if i in self.accounts.keys():
      return i
    for acct_type in self.accounts.keys():
      for acct in self.accounts[acct_type].keys():
          if isinstance(i, str):
              if self.accounts[acct_type][acct].label == i:
                return self.accounts[acct_type][acct]
          if isinstance(i, int):
              if self.accounts[acct_type][acct].code == i:
                return self.accounts[acct_type][acct]
    raise PortfolioAccountError('Account %s not found in %s' % (i, self.__class__.__name__))
  
  def __contains__(self, acct):
    try:
      self[acct]
    except PortfolioAccountError:
      return False
    return True
        
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

  def add_cash_account(self, code):
    name = 'Cash'
    assert name not in self.accounts['Assets'].keys(), "That asset account already exists"
    assert code not in self.all_codes, "That code is already being used"
    self.accounts['Assets'][name] = cash_account(code)
    self.all_codes.add(code)
    
  def add_liability_category(self, name, code, activity=None):
    assert name not in self.accounts['Liabilities'].keys(), "That liability account already exists"
    assert code not in self.all_codes, "That code is already being used"
    self.accounts['Liabilities'][name] = liabilities_account(name, code, activity)
    self.all_codes.add(code)

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


if __name__ == '__main__':
  from ..examples.big_dog_carworks import BigDog

  assert 'Cash' in BigDog, "Could not find Cash account in BigDog"

  
  
