class tax_entity:
  def __init__(self, income_tax_rate=0.):
    self.rates = {'income':income_tax_rate}

  def __repr__(self):
    cls = self.__class__.__name__
    rates = self.rates
    return f'<{cls}>:\n{rates}\n'

  def __iter__(self):
    for key in self.rates.keys():
      yield key

  def __getitem__(self, i):
    return self.rates[i]

  def income_tax(self, net_income):
    if net_income <= 0: return 0
    return net_income * self.rates['income']

  def add_rate(self, name, rate):
    self.rates[name] = rate
    
    
class individual(tax_entity):
  def __init__(self, name, filing_jointly=True):
    tax_entity.__init__(self)
    self.name = name
    self.set_filing(filing_jointly)
    self.brackets = {'rates' : [0.10, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37],
                     'income' : {'single':[0, 9875, 40125, 85525, 163300, 207350, 518400],
                                 'jointly':[0, 19750, 80250, 171050, 326600, 414700, 622050]}}

  def __repr__(self):
    cls = self.__class__.__name__
    rates = self.rates
    name = self.name
    return f'<{cls}>:\n{name}\n{rates}\n'

  def set_filing(self, filing_jointly):
    assert type(filing_jointly) is type(bool()), 'filing_jointly needs to be boolean'
    self.filing_jointly = filing_jointly

  def income_tax(self, annual_wages):
    i = 0
    if self.filing_jointly: filing='jointly'
    else: filing='single'
    for each in self.brackets['income'][filing]:
      if annual_wages <= each: break
      i += 1
    self.rates['income'] = self.brackets['rates'][i] 
    return self.rates['income']*annual_wages
    
    
class employee(individual):
  def __init__(self, name, filing_jointly=True):
    self.name = name
    individual.__init__(self, name=name, filing_jointly=filing_jointly)
    self.add_rate('SS', 0.0622)
    self.add_rate('Medicare', 0.0145)
    self.add_rate('Employer income', 0.015)
    self.employer_share_of_employee_taxes = 0.2

  def wages(self, amount):
    ret = {'from_employer':amount*self['income'], 
           'from_employee':0, 'to_employee':0}
    for each in self:
      if each == 'Employer income': continue
      ret['from_employer'] += self.rates[each]*amount*(1+self.employer_share_of_employee_taxes)
      ret['from_employee'] += self.rates[each]*amount*(1-self.employer_share_of_employee_taxes)
    ret['to_employee'] = amount - ret['from_employee'] - self.income_tax(amount)
    return ret

class self_employed(employee):
  def __init__(self, name, filing_jointly=True):
    self.name = name
    individual.__init__(self, name=name, filing_jointly=filing_jointly)
    self.add_rate('SE', 0.153/2)
    self.employer_share_of_employee_taxes = 0.0
    
    
class corporation(tax_entity):
  def __init__(self, name):
    tax_entity.__init__(self, income_tax_rate=0.21)
    self.name = name
    self.payroll = {}

  def __repr__(self):
    cls = self.__class__.__name__
    rates = self.rates
    name = self.name
    return f'<{cls}>:\n{name}\n{rates}\n'

  def add_to_payroll(self, emp, annual_wages):
    self.payroll[emp] = annual_wages

  def get_payroll_taxes(self):
    ret = {'from_employer':0, 'from_employees':0}
    for emp, annual_wages in self.payroll.items():
      each = emp.wages(annual_wages)
      ret['from_employer'] += each['from_employer']
      ret['from_employees'] += each['from_employee']
    return ret
