from ..taxes.tax_entity import tax_entity

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
