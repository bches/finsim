import numpy as np
from numpy import array


class depreciation:
    '''A base class that can be overridden that defaults to
    straight line depreciation'''
    def __init__(self, initial_value, residual_value, term):
        assert initial_value > 0, "Initial value must be > 0."
        assert 0 < residual_value < initial_value, "Residual value must be > 0, < initial_value."
        assert term > 0, "Term must be > 0."
        self.initial_value = initial_value
        self.residual_value = residual_value
        self.current_value = initial_value
        self.term = term

    def __getitem__(self, i):
        return 1.0 / self.term
        
    def __iter__(self):
        for each in range(self.term):
            yield self(self[each])

    def __call__(self, pct):
        self.current_value -= (self.initial_value - self.residual_value) * pct
        return self.current_value

    def accumulated(self):
        return self.initial_value - self.current_value
    

class straight_line(depreciation):
    pass


class convention:
    def __init__(self, recovery_period_in_years):
        self.depreciation_table = [] * recovery_period_in_years

    def __repr__(self):
        s = '<Instance of %s at %s:\n' % (self.__class__.__name__,
                                          id(self))
        s += 'recovery_period = %d years,' % (len(self)-1)
        s += 'percent = %s>' % self.depreciation_table
        return s
        
    def __len__(self):
        return len(self.depreciation_table)

    def __iter__(self):
        for percent in self.depreciation_table:
            yield percent

    def __getitem__(self, i):
        return self.depreciation_table[i]
            

class half_year(convention):
    '''Table A1 from IRS publication 946'''
    def __init__(self, recovery_period_in_years):
        assert recovery_period_in_years in {3,5,7,10,15,20}, 'Recovery period must be 3, 5, 7, 10, 15, or 20 years'
        if recovery_period_in_years == 3:
            self.depreciation_table = array([33.33, 44.45, 14.81, 7.41]) / 100.0
        elif recovery_period_in_years == 5:
            self.depreciation_table = array([20.00, 32.00, 19.20, 11.52,
                                       11.52, 5.76]) / 100.0
        elif recovery_period_in_years == 7:
            self.depreciation_table = array([14.29, 24.49, 17.49, 12.49,
                                       8.93, 8.92, 8.93, 4.46]) / 100.0
        elif recovery_period_in_years == 10:
            self.depreciation_table = array([10.00, 18.00, 14.40, 11.52,
                                       9.22, 7.37, 6.55, 6.55,
                                       6.56, 6.55, 3.28]) / 100.0
        elif recovery_period_in_years == 15:
            self.depreciation_table = array([5.00, 9.50, 8.55, 7.70,
                                       6.93, 6.23, 5.90, 5.90,
                                       5.91, 5.90, 5.91, 5.90,
                                       5.91, 5.90, 5.91, 2.95]) / 100.0
        elif recovery_period_in_years == 20:
            self.depreciation_table = array([3.750, 7.219, 6.677, 6.177,
                                       5.713, 5.285, 4.888, 4.522,
                                       4.462, 4.461, 4.462, 4.461,
                                       4.462, 4.461, 4.462, 4.461,
                                       4.462, 4.461, 4.462, 4.461,
                                       2.231]) / 100.0

        
class mid_quarter(convention):
    '''Tables A2, A3, A4, A5 from IRS publication 946'''
    def __init__(self, recovery_period_in_years,
                 quarter_placed_in_service):
        assert recovery_period_in_years in {3,5,7,10,15,20}, 'Recovery period must be 3, 5, 7, 10, 15, or 20 years'
        assert 1 <= quarter_placed_in_service <= 4, "Quarter placed in service must be between 1 and 4."
        if recovery_period_in_years == 3:
            if quarter_placed_in_service == 1:
                self.depreciation_table = array([58.33, 27.78, 12.35, 1.54]) / 100.0
            if quarter_placed_in_service == 2:
                self.depreciation_table = array([41.67, 38.89, 14.14, 5.30]) / 100.0
            if quarter_placed_in_service == 3:
                self.depreciation_table = array([25.00, 50.00, 16.67, 8.33]) / 100.0
            if quarter_placed_in_service == 4:
                self.depreciation_table = array([8.33, 61.11, 20.37, 10.19]) / 100.0
        elif recovery_period_in_years == 5:
            if quarter_placed_in_service == 1:
                self.depreciation_table = array([35.00, 26.00, 15.60, 11.01,
                                           11.01, 1.38]) / 100.0
            if quarter_placed_in_service == 2:
                self.depreciation_table = array([25.00, 30.00, 18.00, 11.37,
                                           11.37, 4.26]) / 100.0
            if quarter_placed_in_service == 3:
                self.depreciation_table = array([15.00, 34.00, 20.40, 12.24,
                                           11.30, 7.06]) / 100.0
            if quarter_placed_in_service == 4:
                self.depreciation_table = array([5.00, 38.00, 22.80, 13.68,
                                           10.94, 9.58]) / 100.0
        elif recovery_period_in_years == 7:
            if quarter_placed_in_service == 1:
                self.depreciation_table = array([25.00, 21.43, 15.31, 10.93,
                                           8.75, 8.74, 8.75, 1.09]) / 100.0
            if quarter_placed_in_service == 2:
                self.depreciation_table = array([17.85, 23.47, 16.76, 11.97,
                                           8.87, 8.87, 8.87, 3.34]) / 100.0
            if quarter_placed_in_service == 3:
                self.depreciation_table = array([10.71, 25.51, 18.22, 13.02,
                                           9.30, 8.85, 8.86, 5.53]) / 100.0
            if quarter_placed_in_service == 4:
                self.depreciation_table = array([3.57, 27.55, 19.68, 14.06,
                                           10.04, 8.73, 8.73, 7.64]) / 100.0
        elif recovery_period_in_years == 10:
            if quarter_placed_in_service == 1:
                self.depreciation_table = array([17.50, 16.50, 13.20, 10.56,
                                           8.45, 6.76, 6.55, 6.55,
                                           6.56, 6.55, 0.82]) / 100.0
            if quarter_placed_in_service == 2:
                self.depreciation_table = array([12.50, 17.50, 14.00, 11.20,
                                           8.96, 7.17, 6.55, 6.55,
                                           6.56, 6.55, 2.46]) / 100.0
            if quarter_placed_in_service == 3:
                self.depreciation_table = array([7.50, 18.50, 14.80, 11.84,
                                           9.47, 7.58, 6.55, 6.55,
                                           6.56, 6.55, 4.10]) / 100.0
            if quarter_placed_in_service == 4:
                self.depreciation_table = array([2.50, 19.50, 15.60, 12.48,
                                           9.98, 7.99, 6.55, 6.55,
                                           6.56, 6.55, 5.74]) / 100.0
        elif recovery_period_in_years == 15:
            if quarter_placed_in_service == 1:
                self.depreciation_table = array([8.75, 9.13, 8.21, 7.39,
                                           6.65, 5.99, 5.90, 5.91,
                                           5.90, 5.91, 5.90, 5.91,
                                           5.90, 5.91, 5.90, 0.74]) / 100.0
            if quarter_placed_in_service == 2:
                self.depreciation_table = array([6.25, 9.38, 8.44, 7.59,
                                           6.83, 6.15, 5.91, 5.90,
                                           5.91, 5.90, 5.91, 5.90,
                                           5.91, 5.90, 5.91, 2.21]) / 100.0
            if quarter_placed_in_service == 3:
                self.depreciation_table = array([3.75, 9.63, 8.66, 7.80,
                                           7.02, 6.31, 5.90, 5.90,
                                           5.91, 5.90, 5.91, 5.90,
                                           5.91, 5.90, 5.91, 3.69]) / 100.0
            if quarter_placed_in_service == 4:
                self.depreciation_table = array([1.25, 9.88, 8.89, 8.00,
                                           7.20, 6.48, 5.90, 5.90,
                                           5.90, 5.91, 5.90, 5.91,
                                           5.90, 5.91, 5.90, 5.17]) / 100.0
        elif recovery_period_in_years == 20:
            if quarter_placed_in_service == 1:
                self.depreciation_table = array([6.563, 7.000, 6.482, 5.996,
                                           5.546, 5.130, 4.746, 4.459,
                                           4.459, 4.459, 4.459, 4.460,
                                           4.459, 4.460, 4.459, 4.460,
                                           4.459, 4.460, 4.459, 4.460,
                                           0.565]) / 100.0
            if quarter_placed_in_service == 2:
                self.depreciation_table = array([4.688, 7.148, 6.612, 6.116,
                                           5.658, 5.233, 4.841, 4.478,
                                           4.463, 4.463, 4.463, 4.463,
                                           4.463, 4.463, 4.462, 4.463,
                                           4.462, 4.463, 4.462, 4.463,
                                           1.673]) / 100.0
            if quarter_placed_in_service == 3:
                self.depreciation_table = array([2.813, 7.289, 6.742, 6.237,
                                           5.769, 5.336, 4.936, 4.566,
                                           4.460, 4.460, 4.460, 4.460,
                                           4.461, 4.460, 4.461, 4.460,
                                           4.461, 4.460, 4.461, 4.460,
                                           2.788]) / 100.0
            if quarter_placed_in_service == 4:
                self.depreciation_table = array([0.938, 7.430, 6.872, 6.357,
                                           5.880, 5.439, 5.031, 4.654,
                                           4.458, 4.458, 4.458, 4.458,
                                           4.458, 4.458, 4.458, 4.458,
                                           4.458, 4.459, 4.458, 4.459,
                                           3.901]) / 100.0


class mid_month(convention):
    def __init__(self, recovery_period_in_years,
                 month_placed_in_service):
        assert 1 <= month_placed_in_service <= 12, "Month placed in service must be between 1 (Jan) and 12 (Dec)"
        assert recovery_period_in_years == 27.5 or recovery_period_in_years == 31.5 or recovery_period_in_years == 39, "Recovery period for mid-month convention must be 27.5, 31.5 or 39 years"
        if recovery_period_in_years == 27.5:
            depreciation_table = np.zeros((29, 12))
            depreciation_table[0,:] = array([3.485, 3.182, 2.879, 2.576, 2.273, 1.970, 1.667, 1.364, 1.061, 0.758, 0.455, 0.152]) / 100.0
            depreciation_table[1:8,:] = array([3.636] * 12) / 100.0
            depreciation_table[9:26:2,:] = array([3.637] * 6 + [3.636] * 6) / 100.0
            depreciation_table[10:26:2,:] = array([3.636] * 6 + [3.637] * 6) / 100.0
            depreciation_table[27,:] = array([1.97, 2.273, 2.576, 2.879, 3.182, 3.485] + [3.636]*6) / 100.0
            depreciation_table[28,6:] = array([0.152, 0.455, 0.758, 1.061, 1.364, 1.667]) / 100.0
        elif recovery_period_in_years == 31.5:
            depreciation_table = np.zeros((33,12))
            depreciation_table[0,:] = array([3.042, 2.778, 2.513, 2.249, 1.984, 1.720, 1.455, 1.190, 0.926, 0.661, 0.397, 0.132]) / 100.0
            depreciation_table[1-6,:] = array([3.175] * 12) / 100.0
            depreciation_table[7:30:2,:] = array([3.175, 3.174] * 6) / 100.0
            depreciation_table[8:30:2,:] = array([3.174, 3.175] * 6) / 100.0
            depreciation_table[31,:] = array([1.720, 1.984, 2.249, 2.513, 2.778, 3.042] + [3.175, 3.174] * 6) / 100.0
            depreciation_table[32,6:] = array([0.312, 0.397, 0.661, 0.926, 1.190, 1.455]) / 100.0
        elif recovery_period_in_years == 39:
            depreciation_table = np.zeros((40,12))
            depreciation_table = array([2.461, 2.247, 2.033, 1.819, 1.605, 1.391, 1.177, 0.963, 0.749, 0.535, 0.321, 0.107]) / 100.0
            depreciation_table[1:38,:] = array([2.564] * 12) / 100.0
            depreciation_table[39,:] = array([0.107, 0.321, 0.535, 0.749, 0.963, 1.177, 1.391, 1.605, 1.819, 2.033, 2.247, 2.461]) / 100.0
        self.depreciation_table = depreciation_table[:,month_placed_in_service]
        

# Todo: section 179, bonus, unit of production method


if __name__ == '__main__':


    dut = straight_line(initial_value = 5000,
                        residual_value = 2000,
                        term = 4)

    for value in dut:
        print('value = %d' % value)

        
