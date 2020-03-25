from ..accounting.portfolio import portfolio
from ..accounting.account import equity_account
from ..accounting.adjusting_entry import adjusting_entry


class service_provider(portfolio):
    def __init__(self, name):
        portfolio.__init__(self, name)
        self.accounts['Revenues'] = {}
        self.add_asset_category(name='Accounts Receivable', code=110)
        
    def add_revenue_category(self, name, code):
        assert name not in self.accounts['Revenues'].keys(), "That revenue account already exists"
        assert code not in self.all_codes, "That code is already being used"
        self.accounts['Revenues'][name] = equity_account(name, code, activity='Operating')
        self.all_codes.add(code)

    def receive_payment(self, revenue, amount, total=None):
        self.accounts['Assets']['Cash'].increase(amount)
        if total == None: total = amount
        if total > amount:
            self.accounts['Assets']['Accounts Receivable'].increase(total-amount)
        self.accounts['Revenues'][revenue].increase(total)

    def adjust_unearned_liabilities(self, revenue, amount, description):
        '''Adjust an unearned liability for the amount earned'''
        adj = adjusting_entry(debit_account=self.accounts['Liabilities']['Unearned Revenue'],
                              credit_account=self.accounts['Revenues']['%s Revenues' % revenue])
        adj(amount, description)
        return adj

    def adjust_unearned_revenue(self, revenue, amount, description):
        '''Earn revenue'''
        adj = adjusting_entry(debit_account=self.accounts['Liabilities']['Unearned Revenue'],
                              credit_account=self.accounts['Revenues']['%s Revenues' % revenue])
        adj(amount, description)
        return adj

    def adjust_accrued_revenue(self, revenue, amount, description):
        '''Accrue revenue'''
        adj = adjusting_entry(debit_account=self.accounts['Assets']['Accounts Receivable'],
                              credit_account=self.accounts['Revenues']['%s Revenues' % revenue])
        adj(amount, description)
        return adj
