from decimaldate import DecimalDateRange

TUESDAY = 1

for dd in [
    dd
    for dd in DecimalDateRange.range_month_of_decimal_date(2024_02_14)
    if dd.weekday() == TUESDAY
]:
    print(repr(dd))
