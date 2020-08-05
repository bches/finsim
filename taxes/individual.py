from ..taxes.tax_account import tax_account


class individual(tax_account):
    def __init__(self, name, taxing, filing_jointly=True):
        tax_account.__init__(self, tax_rate=0, taxing=taxing)
        self.name = name
        self.set_filing(filing_jointly)
        # 2020 tables - https://www.irs.gov/pub/irs-pdf/p15t.pdf
        self.brackets = {'rates': [0.0, 0.12, 0.22, 0.24,
                                   0.32, 0.35, 0.37],
                         'income': {'single': [0, 9875, 40125,
                                               85525, 163300,
                                               207350, 518400],
                                    'jointly': [0, 19750, 80250,
                                                171050, 326600,
                                                414700, 622050]}}

    def __repr__(self):
        cls = self.__class__.__name__
        name = self.name
        filing = self.filing_jointly
        acct = tax_account.__repr__(self)
        return f'<{cls} {name}>:\n{acct}\nfiling_jointly={filing}'

    def set_filing(self, filing_jointly):
        assert isinstance(filing_jointly, bool), 'filing_jointly needs to be boolean'
        self.filing_jointly = filing_jointly

    def set_income_tax_rate(self, annual_wages):
        i = 0
        if self.filing_jointly:
            filing = 'jointly'
        else:
            filing = 'single'
        for each in self.brackets['income'][filing]:
            if annual_wages <= each:
                break
            i += 1
        self.tax_rate = self.brackets['rates'][i]
        return self.tax_rate


if __name__ == '__main__':
    from ..taxes.taxing_entity import taxing_entity

    irs = taxing_entity()
    alice = individual(name='Alice',
                       taxing=irs,
                       filing_jointly=False)
    bob = individual(name='Bob',
                     taxing=irs)

    alice.set_income_tax_rate(24000)
    alice.incur_tax(24000/12.)
    alice.pay_tax(210)
    print(alice)
