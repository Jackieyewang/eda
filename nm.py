def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def tran(value):
    if value[-1] == 'f':
        value = float(value[:-1]+'e-15')
    elif value[-1] == 'p':
        value = float(value[:-1]+'e-12')
    elif value[-1] == 'n':
        value = float(value[:-1]+'e-9')
    elif value[-1] == 'u':
        value = float(value[:-1]+'e-6')
    elif value[-1] == 'm':
        value = float(value[:-1]+'e-3')
    elif value[-1] == 'k':
        value = float(value[:-1]+'e3')
    elif value[-1] == 'meg':
        value = float(value[:-1]+'e6')
    elif value[-1] == 'g':
        value = float(value[:-1]+'e9')
    elif value[-1] == 't':
        value = float(value[:-1]+'e12')
    else :
        value = float(value)
    return value
