from ..accounting.vote import vote
from ..accounting.portfolio import portfolio
from ..accounting.account import equity_account, dividends_account


class shares(portfolio):
    def __init__(self, name):
        portfolio.__init__(self, name)
        self.accounts['Equity'] = {}
        self.accounts['Equity']['Share Capital'] = equity_account('Share Capital',
                                                                  320,
                                                                  activity='Financing')
        self.accounts['Equity']['Dividends'] = dividends_account('Dividends',
                                                                 330,
                                                                 activity='Financing')
        self.all_codes.update({320, 330})
        self.shareholders = [{}]
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
        

if __name__ == '__main__':
    dut = shares('Shared Company')

    dut.allocate_shares(cls=0, number_of_shares=10000)
    dut.sell_shares(who='me', cls=0, number_of_shares=1000,
                    capital_raised=10000)
    print(dut)
