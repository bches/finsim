from ..accounting.merchandiser import merchandiser
from ..taxes.corporation import corporation
from ..taxes.individual import individual
from ..taxes.employee import employee
from ..accounting.inventory import inventory, inventory_item
from ..accounting.shares import shares

# The LED There Be Light corporation is totally fictional
# and specializes in manufacturing LEDs and solar panels

class led_there_be_light(merchandiser, shares, corporation):
    def __init__(self, name='LED There Be Light Corp.'):
        merchandiser.__init__(self, name)
        shares.__init__(self, name)
        corporation.__init__(self, name)

        # The owners
        alice = individual(name='Alice', filing_jointly=False)
        bob = individual(name='Bob')

        # shares of the company
        self.allocate_shares(cls=0, number_of_shares=10000)
        self.sell_shares(who=alice, cls=0, number_of_shares=1000,
                         capital_raised=10000)
        self.sell_shares(who=bob, cls=0, number_of_shares=500,
                         capital_raised=5000)

        # The employees
        carol = employee('Carol')
        david = employee('David', filing_jointly=False)
        employees = {david: 100000,
                     carol: 60000}
        for each, annual_wage in employees.items():
            self.add_to_payroll(each, annual_wage)

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
#        inv = inventory(merchandiser=LEDthere)
#        inv.add_inventory_item(leds)
#        inv.add_inventory_item(solar_panels)

    
LEDthere = led_there_be_light()


if __name__ == '__main__':
    print(LEDthere)
