from ..accounting.account import cash_account


class tax_entity:
    def __init__(self, income_tax_rate=0.):
        self.tax_rates = {'income_tax': income_tax_rate}
        try:
            if 'Cash' not in self:
                self.accounts = {'Cash': cash_account(code=101)}
        except TypeError:
            self.accounts = {'Cash': cash_account(code=101)}

    def __repr__(self):
        cls = self.__class__.__name__
        rates = self.tax_rates
        accounts = self.accounts
        return f'<{cls}>:\n{rates}\n{accounts}'

    def income_tax(self, net_income):
        if net_income <= 0:
            return 0
        return net_income * self.tax_rates['income']

    def add_rate(self, name, rate):
        self.tax_rates[name] = rate


if __name__ == '__main__':
    dut = tax_entity()
    print(dut)
