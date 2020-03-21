from ..accounting.account import liabilities_account

class inventory(liabilities_account):
    def __init__(self, label, units='units'):
        self.label = label
        self.units = units
        self._cr = [0]
        self._dr = [0]

    def __repr__(self):
        return '{:>{width}} : [{}]\n\
        {}\n{:{prec}}|{:{prec}}\n'.format(self.label,
                                          self.units, '-'*21,
                                          sum(self._dr),
                                          sum(self._cr),
                                          width=10, prec=10)
