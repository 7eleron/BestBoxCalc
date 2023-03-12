from details.algprog.toFix import toFixed
from cub_box_0.models import PressFoil, Material, Printing


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
    print("--- calc_sum_all ", calc_sum_all)
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


# тиснение наценка
def pressfoil_calc(request, kol):
    request = [int(x) for x in request]
    if len(request) == 3:
        price_klishe = Material.objects.get(mt_type='Клише').prise
        price_preparation_all = PressFoil.objects.all()
        price_preparation = 0
        price_push = 0
        for j in range(len(price_preparation_all)):
            if price_preparation_all[j].quantity <= kol:
                price_preparation = price_preparation_all[j].preparation
                price_push = price_preparation_all[j].push
            else:
                break
        klishe = ((request[1] * request[2]) / 100) * price_klishe
        preparation = request[0] * price_preparation
        push = (kol * price_push) * request[0]
        return {
            'цена': klishe + preparation + push,
            'информация': f' цена клише {klishe}, приладка {preparation}, оттиски {push}.',
                }
    elif len(request) == 4:
        klishe = request[0]
        preparation = request[2]
        push = kol * request[1]
        return {
            'цена': klishe + preparation + push,
            'информация': f'цена клише {klishe}, приладка {preparation}, оттиски {push}.',
        }
    else:
        return {
            'цена': 0,
            'информация': 'нету.',
        }


# шелкография наценка
def pattern_calc(request, kol):
    request = [int(x) for x in request]
    if len(request) == 3:
        netting = Material.objects.get(mt_type='Шелкография').prise * request[0]
        price_preparation_all = Printing.objects.all()
        price_preparation = 0
        price_push = 0
        for j in range(len(price_preparation_all)):
            if price_preparation_all[j].quantity <= kol:
                price_preparation = price_preparation_all[j].preparation
                price_push = price_preparation_all[j].push
            else:
                break
        preparation = request[0] * price_preparation
        push = (kol * price_push) * request[0]
        return {
            'цена': netting + preparation + push,
            'информация': f'цена подготовка {netting}, приладки {preparation}, оттиска {push}.',
        }
    elif len(request) == 4:
        netting = request[0]
        preparation = request[2]
        push = kol * request[1]
        return {
            'цена': netting + preparation + push,
            'информация': f'цена подготовка {netting}, приладки {preparation}, оттиска {push}.',
        }
    else:
        return {
            'цена': 0,
            'информация': 'нету.',
        }


# ложементы наценка
def logement_calc(sum: float):
    return sum
