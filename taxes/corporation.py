from ..taxes.tax_entity import tax_entity
from ..accounting.account import InsufficientFundsError
from ..accounting.portfolio import portfolio


class corporation(tax_entity, portfolio):
    def __init__(self, name):
        tax_entity.__init__(self, income_tax_rate=0.21)
        portfolio.__init__(self, name)
        self.name = name
        self.payroll = {}
        self.add_expense_category('Salaries Expense', 620)
        self.add_liabilities_category('Payroll Tax Witholding', 231)

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

    def run_payroll(self, pay_period, tax_period):
        assert 0 < pay_period <= 1.0, 'Pay period must be > 0. and <= 1.'
        assert pay_period < tax_period <= 1.0, 'Tax period must be > pay_period and <= 1.'
        payroll_taxes = sum([amount for _, amount in self.get_payroll_taxes().items()])
        # make sure there's enough to pay, if not raise InsufficientFundsError
        period_total_salary = 0.
        for each, pay in self.payroll.items():
            period_total_salary += pay
            # transfer cash to employees
            each['Cash'].increase(pay)
        # expense salaries for the period
        self.accounts['Expenses']['Salaries'].increase(period_total_salary)
        # increase Payroll Witholding liability
        self.accounts['Liabilities']['Payroll Tax Witholding'].increase(payroll_taxes)
        # transfer Payroll Witholding to tax collecting
        #   entity if its time
        return


if __name__ == '__main__':
    dut = corporation(name='My Corp.')
    
    # The employees
    carol = employee('Carol')
    david = employee('David', filing_jointly=False)
    employees = {david: 100000, carol: 60000}
    
    for each, annual_wage in employees.items():
        dut.add_to_payroll(each, annual_wage)

    pay_period = 1.0/12
    tax_period = 1.0/4

    for i in range(4):
        for j in range(3):
            dut.run_payroll(pay_period=pay_period,
                            tax_period=tax_period)
        
