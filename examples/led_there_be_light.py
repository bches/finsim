from ..accounting.merchandiser import merchandiser
from ..taxes.corporation import corporation
from ..taxes.employee import employee
from ..accounting.inventory import inventory, inventory_item

# The LED There Be Light corporation is totally fictional
# and specializes in manufacturing LEDs and solar panels

# The pieces of the company
LEDthere = merchandiser('LED There Be Light Corp.')
corp = corporation(LEDthere.name)

# The employees
employees = {employee('Alice', filing_jointly=False): 100000,
             employee('Bob'): 60000}
for each, annual_wage in employees.items():
    corp.add_to_payroll(each, annual_wage)

# The inventory of:
#   solar panels [200 pcs]
#   LEDs [10000 pcs]
leds = inventory_item(label='LED', units='pcs',
                      buy=0.5, sell=1.0)
leds.increase(10000)
solar_panels = inventory_item(label='Solar Panels',
                              units='pcs',
                              buy=75, sell=100)
solar_panels.increase(200)
inv = inventory(merchandiser=LEDthere)
inv.add_inventory_item(leds)
inv.add_inventory_item(solar_panels)

    

if __name__ == '__main__':
    print(LEDthere)
    print()
    print(corp)
    print()
    print(inv)
