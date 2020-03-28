from ..taxes.tax_entity import tax_entity
from ..accounting.account import InsufficientFundsError


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

    def run_payroll(self, period):
        assert 0 < period <= 1.0, 'Period must be > 0. and <= 1.'
        return


if __name__ == '__main__':
    dut = corporation(name='My Corp.')
    
    # The employees
    carol = employee('Carol')
    david = employee('David', filing_jointly=False)
    employees = {david: 100000, carol: 60000}
    
    for each, annual_wage in employees.items():
        dut.add_to_payroll(each, annual_wage)
