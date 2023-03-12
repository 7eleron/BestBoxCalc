import math
from cub_box_0.models import Material
from services.showdetailcalc import show


def material_information(material: str):
    material = material.split(';')
    # получение данных материала из бд
    if len(material) == 1:
        if material[0] == 'Полноцветная печать 170 г/м2':
            # толщина
            thickness = 0.15
            # размер листа материала
            lissiz = [1000, 700]
        else:
            # толщина
            thickness = Material.objects.get(mt_name=material[0]).len
            # размер листа материала
            lissiz = [Material.objects.get(mt_name=material[0]).size_x,
                      Material.objects.get(mt_name=material[0]).size_y]

        return {'name': material[0],
                'thickness': thickness,
                'lissiz': lissiz}
    # получение данных материала от клиента
    else:
        return {'name': material[0],
                'thickness': float(material[3]),
                'lissiz': [int(material[1]), int(material[2])]}


def paperlistsize(expendit: int):
    namepaper = None
    if expendit <= 0.25 and expendit >= 0:
        namepaper = 'Полноцветная печать 170 г/м2 А3'
    elif expendit >= 0.26 and expendit <= 0.5:
        namepaper = 'Полноцветная печать 170 г/м2 А2'
    elif expendit >= 0.51:
        namepaper = 'Полноцветная печать 170 г/м2 А1'
    return namepaper


def search_price_list_count(material_name: str, number_sheets: int):
    price = 0
    sheets_number = 0
    for x in Material.objects.all():
        if x.mt_name == material_name:
            if x.len >= number_sheets:
                price = x.prise
                sheets_number = x.len
                break
            else:
                maxcount = number_sheets // x.len
                maxcountprice = maxcount * x.prise
                mincount = number_sheets % x.len
                mincountprice = 0
                for j in Material.objects.all():
                    if j.mt_name == material_name and j.len <= mincount:
                        mincountprice = j.prise
                price = maxcountprice + mincountprice
                sheets_number = maxcount + mincount
    if show:
        print(f'search price - {price}.'
              f'number_sheets - {number_sheets}.')
    return {'price': price,
            'number_sheets': sheets_number}


def material_price(material: str, kol: int, expenditure: int):
    material = material.split(';')
    if material[0] == 'Полноцветная печать 170 г/м2':
        number_sheets = kol
        price = 0
        if expenditure >= 1:
            expenditure_split = str(expenditure).split('.')
            expenditure_split[1] = '0' + '.' + expenditure_split[1]
            for expend in expenditure_split:
                if float(expend) != 0:
                    run = math.ceil(float(expend))
                    # определение размера листа
                    material_size = paperlistsize(float(expend))
                    # цена
                    pre_price = search_price_list_count(material_size, number_sheets)
                    price += (pre_price['price'] / kol) * run
                    material[0] += f' {material_size[-2:]} {int(pre_price["number_sheets"])}л'
        else:
            run = 1
            # определение размера листа
            material[0] = paperlistsize(expenditure)
            # цена
            pre_price = search_price_list_count(material[0], number_sheets)
            price = (pre_price['price'] / kol) * run
            material[0] = f'{paperlistsize(expenditure)} {int(pre_price["number_sheets"])}л'

        # валюта
        currency = 'rub'

    elif len(material) > 1:
        # цена
        price = float(material[4])
        # валюта
        currency = material[5]
    else:
        # цена
        price = Material.objects.get(mt_name=material[0]).prise
        # валюта
        currency = Material.objects.get(mt_name=material[0]).currency
    if show:
        print(f'material - {material[0]},'
              f'\nprise - {price},'
              f'\ncurrency - {currency}')
    return {'material': material[0],
            'price': price,
            'currency': currency}


def cardboard_search_price(material: str):
    material = material.split(';')
    if len(material) > 1:
        # цена
        price = float(material[4])
        # валюта
        currency = material[5]
    else:
        # валюта
        currency = Material.objects.get(mt_name=material[0]).currency
        # цена
        cardboard = Material.objects.get(mt_name=material[0])
        price = cardboard.prise
    if show:
        print(f'material - {material[0]},'
              f'\nprise - {price},'
              f'\ncurrency - {currency}')
    return {'material': material[0],
            'price': price,
            'currency': currency}


