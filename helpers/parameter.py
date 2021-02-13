import time
import re
import operator


def years(param_years: str, config_min_year: int, config_max_year: int):

    def operations(_year):
        _year = str(_year)
        current_year = time.localtime().tm_year
        ops = {"+": operator.add, "-": operator.sub}  # https://stackoverflow.com/a/1740759

        if r1.match(_year):
            return int(_year)
        elif _year == '0':
            return current_year
        # add/subtract value from year
        elif r3.match(_year):
            _year_op = _year[0:1]
            _year_value = int(_year[1:])
            return ops[_year_op](current_year, _year_value)
        else:
            return None

    r1 = re.compile('^[0-9]{4}$')
    r2 = re.compile('^[0-9]{4}-[0-9]{4}$')
    r3 = re.compile('^[+|-][0-9]+$')

    # return param_years if it is in proper format
    if param_years:
        if r1.match(param_years):
            return str(param_years), int(param_years), int(param_years)
        elif r2.match(param_years):
            return str(param_years), int(param_years.split('-')[0]), int(param_years.split('-')[1])

    if config_min_year is not None:
        new_min_year = operations(config_min_year)
    else:
        new_min_year = None

    if config_max_year is not None:
        new_max_year = operations(config_max_year)
    else:
        new_max_year = None

    if new_min_year and new_max_year:
        new_years = str(new_min_year) + '-' + str(new_max_year)
    elif new_min_year:
        new_years = str(new_min_year)
    elif new_max_year:
        new_years = str(new_max_year)
    else:
        new_years = None

    return new_years, new_min_year, new_max_year
