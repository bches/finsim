from ..taxes.individual import individual


class employee(individual):
    def __init__(self, name, filing_jointly=True):
        self.name = name
        individual.__init__(self, name=name, filing_jointly=filing_jointly)
        self.add_rate('SS', 0.0620)
        self.add_rate('Medicare', 0.0145)

    def pay(self, net_pay):
        self.accounts['Cash'].increase(net_pay)

    def payroll_tax(self, amount, employer_share=0.2):
        # for 2020 social security witholding maxes out at $137,700
        return sum([amount * tax for _, tax in self.tax_rates.items()])

    def income_tax_witheld(self, annual_wage, pay_period):
        assert 0 < pay_period <= 1.0, "Pay period must be > 0 and <= 1"
        return pay_period * individual.income_tax(self, annual_wage)

      
class self_employed(employee):
    def __init__(self, name, filing_jointly=True):
        self.name = name
        individual.__init__(self, name=name, filing_jointly=filing_jointly)
        self.add_rate('SE', 0.153/2)
        # The OASDI tax rate for self-employment income in 2020 is 12.4 percent


if __name__ == '__main__':
  
    carol = employee('Carol')
    david = employee('David', filing_jointly=False)
    employees = {david: 100000, carol: 24000}
    pay_period = 1./12
    
    for each, annual_wage in employees.items():
      period_wage = pay_period * annual_wage
      payroll_tax = each.payroll_tax(period_wage)
      income_tax_witheld = each.income_tax_witheld(annual_wage,
                                                   pay_period)
      print(each.name)
      print('payroll_tax=', payroll_tax)
      print('income_tax_witheld=', income_tax_witheld)
      each.pay(period_wage - payroll_tax - income_tax_witheld)
      print(each)
      print()
