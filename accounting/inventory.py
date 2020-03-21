from ..accounting.account import liabilities_account


class inventory_item(liabilities_account):
    def __init__(self, label, units='units', buy=0, sell=0):
        liabilities_account.__init__(self, label=label, code=None)
        self.units = units
        self.buy = buy
        self.sell = sell
        
    def __repr__(self):
        buy = self.buy
        sell = self.sell
        return '{:>{width}} : [{}] @ (buy={}, sell={})\n\
        {}\n{:{prec}}|{:{prec}}\n'.format(self.label,
                                          self.units, self.buy, self.sell, '-'*21,
                                          sum(self._dr),
                                          sum(self._cr),
                                          width=10, prec=10)


if __name__ == '__main__':
    leds = inventory_item(label='LED', units='pcs',
                          buy=0.5, sell=1.0)
    leds.increase(10000)
    leds.decrease(1000)
    print(leds)
    print('Net LEDs:', leds())
