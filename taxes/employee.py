from ..taxes.individual import individual
from ..taxes.tax_account import tax_account


class payroll_tax:
    def __init__(self, taxing):
        self.social_security = tax_account(tax_rate=0.062,
                                           taxing=taxing)
        self.medicare = tax_account(tax_rate=0.0145,
                                    taxing=taxing)

    def __repr__(self):
        s = '%s :\n' % (self.__class__.__name__)
        s += str(self.social_security)
        s += str(self.medicare)
        return s

    def incur_tax(self, gross_amount):
        self.social_security.incur_tax(gross_amount)
        self.medicare.incur_tax(gross_amount)

    def pay_tax(self, amount):
        self.social_security.pay_tax(amount)
        self.medicare.pay_tax(amount)
        

class employee(individual, payroll_tax):
    def __init__(self, name, taxing, filing_jointly=True):
        individual.__init__(self, name=name, taxing=taxing,
                            filing_jointly=filing_jointly)
        payroll_tax.__init__(self, taxing=taxing)
        self.payroll_tax_income_limit = 137700
        self.clear_accumulated_wages()
        
    def __repr__(self):
        s = individual.__repr__(self)
        s += payroll_tax.__repr__(self)
        return s

    def clear_accumulated_wages(self):
        self.accumulated_wages = 0

    def gross_pay(self, amount):
        assert amount > 0, "Amount must be > 0"
        residue = self.payroll_tax_income_limit - self.accumulated_wages
        if residue > amount:
            payroll_tax.incur_tax(self, amount)
        elif 0 > residue < amount:
            payroll_tax.incur_tax(self, amount)
        individual.incur_tax(self, amount)
        
        
class self_employed(employee):
    def __init__(self, name, filing_jointly=True):
        self.name = name
        individual.__init__(self, name=name, filing_jointly=filing_jointly)
        self.add_rate('SE', 0.153/2)
        # The OASDI tax rate for self-employment income in 2020 is 12.4 percent


if __name__ == '__main__':
    from ..taxes.taxing_entity import taxing_entity

    irs = taxing_entity()
  
    carol = employee('Carol', taxing=irs)
    david = employee('David', taxing=irs, filing_jointly=False)
    employees = {david: 100000, carol: 24000}
    pay_period = 1./12
    
    for each, annual_wage in employees.items():
      print(each.name)
      each.set_income_tax_rate(annual_wage)
      each.gross_pay(pay_period * annual_wage)
      print(each)
