from ..accounting.account import cash_account


class taxing_entity:
    def __init__(self):
        self.cash = cash_account(code=101)

    def __repr__(self):
        cls = self.__class__.__name__
        accounts = self.cash
        return f'<{cls}>:\n{accounts}'

    def pay(self, amount):
        assert amount > 0, 'Amount must be > 0'
        self.cash.increase(amount)


if __name__ == '__main__':
    dut = tax_entity()
    print(dut)
