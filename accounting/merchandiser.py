from ..accounting.portfolio import portfolio
from ..accounting.account import equity_account
from ..accounting.adjusting_entry import adjusting_entry


class merchandiser(portfolio):
    def __init__(self, name):
        portfolio.__init__(self, name)
        self.accounts['Sales'] = {}
        self.accounts['Inventory'] = {}
        self.add_asset_category(name='Accounts Receivable', code=110)

    def add_sales_category(self, name, code):
        assert name not in self.accounts['Sales'].keys(), "That sales account already exists"
        assert code not in self.all_codes, "That code is already being used"
        self.accounts['Sales'][name] = equity_account(name, code, activity='Operating')
        self.all_codes.add(code)

    def receive_payment(self, revenue, amount, total=None):
        self.accounts['Assets']['Cash'].increase(amount)
        if total == None: total = amount
        if total > amount:
            self.accounts['Assets']['Accounts Receivable'].increase(total-amount)
        self.accounts['Revenues'][revenue].increase(total)
