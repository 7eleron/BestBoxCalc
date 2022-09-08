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


def material_price(material: str, kol: int, expenditure: int):
    material = material.split(';')
    if material[0] == 'Полноцветная печать 170 г/м2':
        if expenditure <= 1:
            lis = 1 // expenditure
            run = 1
            number_sheets = math.ceil(kol / lis)
        else:
            lis = math.ceil(expenditure)
            run = math.ceil(expenditure)
            number_sheets = kol
        # цена
        price = 0
        for x in Material.objects.all():
            if x.mt_name == material[0] and x.len >= number_sheets:
                price = x.prise
                break
        price = (price / kol) * run
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
    return {'price': price,
            'currency': currency}
