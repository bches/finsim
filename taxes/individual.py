from ..taxes.tax_entity import tax_entity


class individual(tax_entity):
    def __init__(self, name, filing_jointly=True):
        tax_entity.__init__(self)
        self.name = name
        self.set_filing(filing_jointly)
        self.brackets = {'rates': [0.10, 0.12, 0.22, 0.24,
                                   0.32, 0.35, 0.37],
                         'income': {'single': [0, 9875, 40125,
                                               85525, 163300,
                                               207350, 518400],
                                    'jointly': [0, 19750, 80250,
                                                171050, 326600,
                                                414700, 622050]}}

    def __repr__(self):
        s = tax_entity.__repr__(self)
        s += '\nname = %s' % self.name
        s += '\nfiling_jointly = %s' % self.filing_jointly
        return s
      
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
        self.rates['income'] = self.brackets['rates'][i]
        return self.rates['income']*annual_wages


if __name__ == '__main__':
    alice = individual(name='Alice', filing_jointly=False)
    bob = individual(name='Bob')

    print(alice)
    print(bob)
