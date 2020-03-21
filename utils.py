def accounting_print(x):
    if x < 0:
        return f'({-1*x})'
    if x > 0:
        return f'{x}'
    return ''
