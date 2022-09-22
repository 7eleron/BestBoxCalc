import math
from cub_box_0.models import Material


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
        print('material', material)
        return {'name': material[0],
                'thickness': float(material[3]),
                'lissiz': [int(material[1]), int(material[2])]}


def paperlistsize(expendit: int):
    namepaper = None
    if expendit <= 0.25:
        namepaper = 'Полноцветная печать 170 г/м2 А3'
    elif expendit >= 0.26 and expendit <= 0.5:
        namepaper = 'Полноцветная печать 170 г/м2 А2'
    elif expendit >= 0.51:
        namepaper = 'Полноцветная печать 170 г/м2 А1'
    return namepaper


def search_price_list_count(material_name: str, number_sheets: int):
    price = 0
    for x in Material.objects.all():
        # print(f'{x.mt_name} == {material_name} and {x.len} >= {number_sheets}')
        if x.mt_name == material_name:
            if x.len >= number_sheets:
                print(f'number_sheets - {number_sheets}; '
                      f'x.len - {x.len};')
                price = x.prise
                print('price ', price)
                break
            else:
                print(f'number_sheets - {number_sheets}; '
                      f'x.len - {x.len}; '
                      f'x.prise - {x.prise}; ')
                maxcount = number_sheets // x.len
                maxcountprice = maxcount * x.prise
                mincount = number_sheets % x.len
                mincountprice = 0
                for j in Material.objects.all():
                    if j.mt_name == material_name and j.len <= mincount:
                        print('list ', j.len)
                        mincountprice = j.prise
                price = maxcountprice + mincountprice
                print(f'maxcount - {maxcount}; '
                      f'maxcountprice - {maxcountprice}; '
                      f'mincount - {mincount}; '
                      f'mincountprice - {mincountprice}; '
                      f'price - {price}.')
    return price


def material_price(material: str, kol: int, expenditure: int):
    material = material.split(';')
    if material[0] == 'Полноцветная печать 170 г/м2':
        if expenditure <= 1:
            lis = 1 // expenditure
            run = 1
            number_sheets = math.ceil(kol / lis)
        else:
            run = math.ceil(expenditure)
            number_sheets = kol
        # определение размера листа
        print(material[0])
        material[0] = paperlistsize(expenditure)
        print(material[0])
        # цена
        pre_price = search_price_list_count(material[0], number_sheets)
        print(pre_price)
        price = (pre_price / kol) * run
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
    print({'price': price,
            'currency': currency})
    return {'price': price,
            'currency': currency}

