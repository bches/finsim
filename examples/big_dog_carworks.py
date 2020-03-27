from ..accounting.service_provider import service_provider
from ..accounting.shares import shares


# The Big Dog Carworks example comes from the Introduction to Financial
# Accounting book, which is available at:
# https://open.umn.edu/opentextbooks/textbooks/215

class big_dog_carworks(service_provider, shares):
    def __init__(self, name='Big Dog Carworks Corp.'):
        service_provider.__init__(self, name=name)
        shares.__init__(self, name=name)

        # transaction 1: Issue 1000 shares for $10000
        self.allocate_shares(cls=0, number_of_shares=10000)
        self.sell_shares(who='Tom', cls=0, number_of_shares=1000,
                         capital_raised=10000)

        # transaction 2: Borrow $3000 from Bank
        self.add_liability_category(name='Bank Loan', code=201, activity='Financing')
        self.borrow(liability='Bank Loan', amount=3000)

        # transaction 3: Purchase $3000 of Equipment
        self.add_asset_category(name='Equipment', code=183, activity='Investing')
        self.purchase_asset(asset='Equipment', amount=3000)

        # transaction 4: Purchase truck for $8000 - pay $3000 in Cash and borrow
        # $5000 from Bank
        self.add_asset_category(name='Truck', code=184, activity='Investing')
        self.finance_asset(asset='Truck', price=8000, liability='Bank Loan',
                             amount_financed=5000)

        # transaction 5: Prepay $2400 for the coming year's insurance
        self.add_asset_category(name='Prepaid Insurance', code=161,
                                  activity='Operating')
        self.purchase_asset(asset='Prepaid Insurance', amount=2400)

        # transaction 6: Pay $2000 to the Bank Loan
        self.pay_liability(liability='Bank Loan', amount=2000)

        # transaction 7: Receive $400 advanced payment on services to be
        # performed in the future
        self.add_liability_category(name='Unearned Revenue', code=247,
                                      activity='Operating')
        self.borrow(liability='Unearned Revenue', amount=400)

        # transaction 8: Book $10000 of Repair Revenue - $8000 in Cash and
        # $2000 to Accounts Receivable
        self.add_revenue_category('Repair Revenues', 500)
        self.receive_payment(revenue='Repair Revenues', amount=8000, total=10000)

        # transaction 9: Record operating expenses paid, the $700 fuel expense
        # was on credit
        self.add_expense_category('Rent Expense', 610)
        self.pay_expense(expense='Rent Expense', amount=1600)

        self.add_expense_category('Salaries Expense', 620)
        self.pay_expense(expense='Salaries Expense', amount=3500)

        self.add_expense_category('Supplies Expense', 630)
        self.pay_expense(expense='Supplies Expense', amount=2000)

        self.add_expense_category('Fuel Expense', 640)
        self.borrow_expense(expense='Fuel Expense', amount=700)

        # transaction 10: pay $200 dividend
        self.allocate_dividends(cls=0, amount=200)

        # Trial Balance Adjustments
        self.adjust_unearned_revenue(revenue='Repair', amount=300,
                                       description='To adjust for unearned revenue.')

        self.add_expense_category(name='Insurance', code=650)
        self.adjust_prepaid_asset(asset='Prepaid Insurance', expense='Insurance',
                                    amount=200,
                                    description='To adjust for the use of one month of \
pre-paid insurance')

        self.add_expense_category(name='Equipment Dep.', code=680)
        self.add_liability_category(name='Acc. Equipment Dep.', code=240)
        self.adjust_depreciate_ppe(asset='Equipment', amount=25,
                                     description='To adjust for one month of depreciation \
on the equipment')

        self.add_expense_category(name='Truck Dep.', code=690)
        self.add_liability_category(name='Acc. Truck Dep.', code=250)
        self.adjust_depreciate_ppe(asset='Truck', amount=100,
                                     description='To adjust for one month of depreciation \
on the truck')

        self.adjust_accrued_revenue(revenue='Repair', amount=400,
                                      description='To adjust for accrued revenue')

        self.add_expense_category(name='Interest Expense', code=660)
        self.add_liability_category(name='Interest Payable', code=220)
        self.adjust_accrued_expenses(expense='Interest', amount=18,
                                       description='To adjust for accrued interest; \
$6000 x 4% x 28/365 = $18.41 (rounded to the nearest dollar)')

        self.add_expense_category(name='Income Tax Expense', code=670)
        self.add_liability_category(name='Income Tax Payable', code=230)
        self.adjust_accrued_expenses(expense='Income Tax', amount=500,
                                       description='To adjust for January accrued \
income tax')


BigDog = big_dog_carworks()


if __name__ == '__main__':
    print(BigDog)
