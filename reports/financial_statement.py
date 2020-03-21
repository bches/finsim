class financial_statement:
    '''Virtual base class for the other financial statements'''
    def __init__(self, co, periodicity, timestamp):
        self.co = co
        self.statement = 'Financial Statement'
        self.ending = 'For the %s Ending %s' % (periodicity, timestamp.ctime())

    def __repr__(self):
        company = self.co.name
        statement = self.statement
        ending = self.ending
        return f'{company}\n\
{statement}\n\
{ending}\n\n'
