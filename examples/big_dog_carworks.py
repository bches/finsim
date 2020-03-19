from ..accounting.portfolio import portfolio

# The Big Dog Carworks example comes from the Introduction to Financial
# Accounting book, which is available at:
# https://open.umn.edu/opentextbooks/textbooks/215

BigDog = portfolio('Big Dog Carworks Corp.')

# transaction 1: Issue 1000 shares for $10000
BigDog.add_equity()
BigDog.allocate_share_capital(10000)

# transaction 2: Borrow $3000 from Bank
BigDog.add_liability_category(name='Bank Loan', code=201, activity='Financing')
BigDog.borrow(liability='Bank Loan', amount=3000)

# transaction 3: Purchase $3000 of Equipment
BigDog.add_asset_category(name='Equipment', code=183, activity='Investing')
BigDog.purchase_asset(asset='Equipment', amount=3000)

# transaction 4: Purchase truck for $8000 - pay $3000 in Cash and borrow $5000 from Bank
BigDog.add_asset_category(name='Truck', code=184, activity='Investing')
BigDog.finance_asset(asset='Truck', price=8000, liability='Bank Loan', amount_financed=5000)

# transaction 5: Prepay $2400 for the coming year's insurance
BigDog.add_asset_category(name='Prepaid Insurance', code=161, activity='Operating')
BigDog.purchase_asset(asset='Prepaid Insurance', amount=2400)

# transaction 6: Pay $2000 to the Bank Loan
BigDog.pay_liability(liability='Bank Loan', amount=2000)

# transaction 7: Receive $400 advanced payment on services to be performed in the future
BigDog.add_liability_category(name='Unearned Revenue', code=247, activity='Operating')
BigDog.borrow(liability='Unearned Revenue', amount=400)

# transaction 8: Book $10000 of Repair Revenue - $8000 in Cash and $2000 to Accounts Receivable
BigDog.add_revenue_category('Repair Revenues', 500)
BigDog.receive_payment(revenue='Repair Revenues', amount=8000, total=10000)

#transaction 9: Record operating expenses paid, the $700 fuel expense was on credit
BigDog.add_expense_category('Rent Expense', 610)
BigDog.pay_expense(expense='Rent Expense', amount=1600)

BigDog.add_expense_category('Salaries Expense', 620)
BigDog.pay_expense(expense='Salaries Expense', amount=3500)

BigDog.add_expense_category('Supplies Expense', 630)
BigDog.pay_expense(expense='Supplies Expense', amount=2000)

BigDog.add_expense_category('Fuel Expense', 640)
BigDog.borrow_expense(expense='Fuel Expense', amount=700)

# transaction 10: pay $200 dividend
BigDog.allocate_dividends(200)

if __name__ == '__main__':
    print(BigDog)
    print()
    
