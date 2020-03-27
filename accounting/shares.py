from ..accounting.vote import vote
from ..accounting.portfolio import portfolio
from ..accounting.account import equity_account, dividends_account


class shares(portfolio):
    def __init__(self, name):
        if 'Cash' not in self:
            portfolio.__init__(self, name)
        self.accounts['Equity'] = {}
        self.accounts['Equity']['Share Capital'] = equity_account('Share Capital',
                                                                  320,
                                                                  activity='Financing')
        self.accounts['Equity']['Dividends'] = dividends_account('Dividends',
                                                                 330,
                                                                 activity='Financing')
        self.all_codes.update({320, 330})
        self.shareholders = []
        self.add_share_class()

    def __repr__(self):
        s = portfolio.__repr__(self)
        s += str(self.shareholders)
        return s
        
    def add_share_class(self):
        self.shareholders += [{'Treasury':None}]
        return len(self.shareholders)

    def allocate_shares(self, cls, number_of_shares):
        N = len(self.shareholders)
        assert 0 <= cls < N, 'Only %d classes of shares' % N
        self.shareholders[cls]['Treasury'] = number_of_shares
    
    def sell_shares(self, who, cls, number_of_shares, capital_raised):
        assert number_of_shares > 0, 'Must be a positive amount of shares'
        assert capital_raised > 0, 'Must be a positive amount of capital'
        N = len(self.shareholders)
        assert 0 <= cls < N, 'Only %d class(es) of shares' % N
        assert number_of_shares <= self.shareholders[cls]['Treasury'], 'Not enough shares in Treasury'
        if who in self.shareholders[cls].keys():
            self.shareholders[cls][who] += number_of_shares
        else:
            self.shareholders[cls][who] = number_of_shares
        self.shareholders[cls]['Treasury'] -= number_of_shares
        self.accounts['Assets']['Cash'].increase(capital_raised)
        self.accounts['Equity']['Share Capital'].increase(capital_raised)

    def transfer_shares(self, _from, _to, cls, number_of_shares):
        assert _from != 'Treasury', 'Cannot transfer shares from the Treasury'
        N = len(self.shareholders)
        assert 0 <= cls < N, 'Only %d class(es) of shares' % N
        assert number_of_shares <= self.shareholders[cls][_from], 'Not enough shares to transfer.'
        assert number_of_shares > 0, "Number of shares must be positive."
        self.shareholders[cls][_from] -= number_of_shares
        if _to in self.shareholders[cls].keys():
            self.shareholders[cls][_to] += number_of_shares
        else:
            self.shareholders[cls][_to] = number_of_shares

    def shares_outstanding(self, cls):
        N = len(self.shareholders)
        assert 0 <= cls < N, 'Only %d class(es) of shares' % N
        return sum([Nshares for holder, Nshares in self.shareholders[cls].items() if holder != 'Treasury'])

    def allocate_dividends(self, cls, amount):
        self.accounts['Assets']['Cash'].decrease(amount)
        self.accounts['Equity']['Dividends'].decrease(amount)


if __name__ == '__main__':
    dut = shares('Shared Company')

    dut.allocate_shares(cls=0, number_of_shares=10000)
    dut.sell_shares(who='me', cls=0, number_of_shares=1000,
                    capital_raised=10000)
    dut.sell_shares(who='you', cls=0, number_of_shares=500,
                    capital_raised=5000)
    dut.transfer_shares(_from='me', _to='them', cls=0,
                        number_of_shares=100)
    print(dut)
    print('shares_outstanding:', dut.shares_outstanding(cls=0))
