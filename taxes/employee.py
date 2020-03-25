from ..taxes.individual import individual

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
    
