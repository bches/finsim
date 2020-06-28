from depreciation import straight_line, mid_month


class real_property(straight_line, mid_month):
    def __init__(self, initial_value, residual_value,
                 recovery_period_in_years, month_placed_in_service): 
        straight_line.__init__(self, initial_value, residual_value,
                               recovery_period_in_years)
        mid_month.__init__(self, recovery_period_in_years,
                           month_placed_in_service)

    def __iter__(self):
        for each in range(mid_month.__len__(self)):
            yield self(mid_month.__getitem__(self, each))

    
class residential_real_property(real_property):
    def __init__(self, initial_value, residual_value,
                 month_placed_in_service):
        real_property.__init__(self, initial_value=initial_value,
                               residual_value=residual_value, 
                               recovery_period_in_years=27.5,
                               month_placed_in_service=month_placed_in_service),
                               


class nonresidential_real_property(real_property):
    def __init__(self, initial_value, residual_value, 
                 recovery_period_in_years,
                 month_placed_in_service):
        assert recovery_period_in_years == 31.5 or recovery_period_in_years == 39, "For nonresidential real property, recovery period must be 31.5 or 39 years"
        real_property.__init__(self, initial_value, residual_value, 
                               recovery_period_in_years,
                               month_placed_in_service)

                
if __name__ == '__main__':
    property = residential_real_property(initial_value = 100000,
                                         residual_value = 10000,
                                         month_placed_in_service = 7)
    print(property)
    print()

    for value in property:
        print('value =', value)

    print()
    print('accumulated_depreciation =', property.accumulated())
    
    
    
