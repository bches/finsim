class tax_entity:
  def __init__(self, income_tax_rate=0.):
    self.rates = {'income':income_tax_rate}

  def __repr__(self):
    cls = self.__class__.__name__
    rates = self.rates
    return f'<{cls}>:\n{rates}\n'

  def __iter__(self):
    for key in self.rates.keys():
      yield key

  def __getitem__(self, i):
    return self.rates[i]

  def income_tax(self, net_income):
    if net_income <= 0: return 0
    return net_income * self.rates['income']

  def add_rate(self, name, rate):
    self.rates[name] = rate
