from details.algprog.toFix import toFixed


def rou(number):
    number = toFixed(number, 2)
    number_f, number_s = int(number.split('.')[0]), int(number.split('.')[1])
    if number_s >= 0 and number_s <= 25:
        number_s = 25
        return float(f'{number_f}.{number_s}')

    elif number_s >= 26 and number_s <= 50:
        number_s = 50
        return float(f'{number_f}.{number_s}')

    elif number_s >= 51 and number_s <= 75:
        number_s = 75
        return float(f'{number_f}.{number_s}')

    elif number_s >= 76:
        number_f += 1
        return number_f
