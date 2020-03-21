from ..accounting.account import liabilities_account


class inventory_item(liabilities_account):
    def __init__(self, label, units='units', buy=0, sell=0):
        liabilities_account.__init__(self, label=label, code=None)
        self.units = units
        self.buy = buy
        self.sell = sell

    def __repr__(self):
        return '{:>{width}} : [{}] @ (buy={}, sell={})\n\
        {}\n{:{prec}}|{:{prec}}\n'.format(self.label,
                                          self.units,
                                          self.buy,
                                          self.sell,
                                          '-'*21,
                                          sum(self._dr),
                                          sum(self._cr),
                                          width=10, prec=10)

    def cost_of_goods_sold(self):
        return self.buy * sum(self._dr)

    def value(self):
        return self.buy * self()

    def sales(self):
        return self.sell * sum(self._dr)

    def reset(self):
        self._cr = []
        self._dr = []

        
class inventory:
    def __init__(self, merchandiser):
        # temporary account
        assert 'Inventory' in merchandiser, 'Merchandiser needs an Inventory category'
        # temporary account
        assert 'Sales' in merchandiser, 'Merchandiser needs a Sales category'
        self.merchandiser = merchandiser
        self.inventoried = set({})

    def __item__(self):
        for i in self.inventoried:
            yield i

    def __getitem__(self, i):
        for each in self:
            if each.label == i:
                return each

    def __call__(self):
        inventory_value = sum([each.value() for each in self])
        self.merchandiser['Inventory'].increase(inventory_value)
        sales = sum([each.sales() for each in self])
        self.merchandiser['Sales'].increase(sales)
            
    def add_inventory_item(self, i):
        self.inventoried.add(i)

    
if __name__ == '__main__':
    leds = inventory_item(label='LED', units='pcs',
                          buy=0.5, sell=1.0)
    leds.increase(10000)
    leds.decrease(1000)
    print(leds)
    print('Net LEDs:', leds())
    print('COGS:', leds.cost_of_goods_sold())
    print('Sales:', leds.sales())
    print('Inventory value:', leds.value())
    print()
    
    solar_panels = inventory_item(label='Solar Panels',
                                  units='pcs',
                                  buy=75, sell=100)
    solar_panels.increase(200)
    print(solar_panels)
    print()
