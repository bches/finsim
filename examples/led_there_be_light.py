from ..accounting.merchandiser import merchandiser
from ..taxes.corporation import corporation
from ..taxes.employee import employee

# The LED There Be Light corporation is totally fictional
# and specializes in manufacturing LEDs and solar panels

LEDthere = merchandiser('LED There Be Light Corp.')
corp = corporation(LEDthere.name)


employees = {employee('Alice', filing_jointly=False): 100000,
             employee('Bob'): 60000}
for each, annual_wage in employees.items():
    corp.add_to_payroll(each, annual_wage)

# transaction 1: Issue 1000 shares for $10000
LEDthere.add_equity()
LEDthere.allocate_share_capital(10000)


if __name__ == '__main__':
    print(LEDthere)
    print()
    print(corp)
