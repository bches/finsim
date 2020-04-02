from ..taxes.tax_entity import tax_entity


class individual(tax_entity):
    def __init__(self, name, filing_jointly=True):
        tax_entity.__init__(self)
        self.name = name
        self.set_filing(filing_jointly)
        # 2020 tables - https://www.irs.gov/pub/irs-pdf/p15t.pdf
        self.brackets = {'rates': [0.0, 0.10, 0.12, 0.22, 0.24,
                                   0.32, 0.35, 0.37],
                         'income': {'single': [0, 9875, 40125,
                                               85525, 163300,
                                               207350, 518400],
                                    'jointly': [0, 19750, 80250,
                                                171050, 326600,
                                                414700, 622050]}}

    def __repr__(self):
        cls = self.__class__.__name__
        rates = self.tax_rates
        accounts = self.accounts
        name = self.name
        filing = self.filing_jointly
        return f'<{cls} {name}>:\n{rates}\n{accounts}\nfiling_jointly={filing}'

    def set_filing(self, filing_jointly):
        assert isinstance(filing_jointly, bool), 'filing_jointly needs to be boolean'
        self.filing_jointly = filing_jointly

    def income_tax(self, annual_wages):
        i = 0
        if self.filing_jointly:
            filing = 'jointly'
        else:
            filing = 'single'
        for each in self.brackets['income'][filing]:
            if annual_wages <= each:
                break
            i += 1
        self.tax_rates['income'] = self.brackets['rates'][i]
        return self.tax_rates['income']*annual_wages


if __name__ == '__main__':
    alice = individual(name='Alice', filing_jointly=False)
    bob = individual(name='Bob')

    print(alice)
    print(bob)

    print('monthly income_tax=', alice.income_tax(annual_wages=24000)/12.)
    print(alice)
