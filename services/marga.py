from details.algprog.toFix import toFixed


# % менеджера
def proc_manager(production_cost: float, uppercost: float, kol: int):
    return {'информация': f'Бонус менеджера: {int(((production_cost * (uppercost / 100)) * 0.1) * kol)} руб.',
            'result': int(((production_cost * (uppercost / 100)) * 0.1) * kol)}


# цена
def prices_one(calc_sum: float, uppercost: float):
    return f'Цена коробки: наценка {int(uppercost)}%, без НДС - {toFixed(calc_sum, 2)} руб./шт.,' \
           f' с НДС - {toFixed(calc_sum * 1.2, 2)} руб./шт.'


# сумма заказа
def count_all(calc_sum_all: float):
    return f'Сумма заказа: без НДС {int(calc_sum_all)} руб., с НДС {int(calc_sum_all*1.2)} руб.'


# маржа заказа
def marga_all(calc_sum_all: float, production_cost_all: int):
    marga = calc_sum_all - production_cost_all
    return f'Маржа: {int(marga)} руб.'


# наценка
def upper_cost(production_cost, upercost: float):
    sum_cost = float(toFixed(((production_cost * (upercost/100)) * 1.1) + production_cost, 2))
    return sum_cost


# склейка двух цен
def glue_price(first: list, second: list):
    calc_sum = []
    for x in range(8):
        calc_sum.append(toFixed(first[x] + second[x], 2))
    return calc_sum
