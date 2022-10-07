from django.utils.safestring import mark_safe

from cub_box_0.models import calc_count, Material
from casketM.calculate import CardboardCasketBox, PaperCasketBox
from details.algprog.round import rou
from details.algprog.toFix import toFixed
from services.marga import prices_one, upper_cost, proc_manager, count_all, marga_all
from services.materialcalculate import material_information, material_price, cardboard_search_price
from services.showdetailcalc import show
from work.hand_work_laminating import laminating_work
from work.auto_work_tray import machin_work_tray
from work.hand_work_folder import folder_work
from work.hand_work_cubbox import hand_work
from services.shtamp.folderm import resp_folder
from services.shtamp.trayflap import resp_tray


def result_data_briefcase(a, b, c, cardboard_req, paper_req, kol, currency_req, handle, laminating, uppercost):
    # материал
    mt_cardboard = material_information(cardboard_req)
    mt_paper = material_information(paper_req)
    cardboard = CardboardCasketBox(width=a, length=b, tray_hight=c, thickness_cb=mt_cardboard["thickness"]
                                   ).cardboard_box(lis_siz=mt_cardboard["lissiz"])
    paper = PaperCasketBox(width=a, length=b, tray_hight=c, thickness_cb=mt_cardboard["thickness"])
    # расход картона
    result_cardboard = cardboard['Расход']
    # расход бумаги, крышка
    paper_lid = paper.lid(mt_paper['lissiz'])
    result_paper_lid = paper_lid['Расход']
    m2_folder = paper_lid['m2']

    # кашировка
    result_laminat_lid = 0
    result_laminat_tray = 0
    result_laminat = 0
    # стоимость работы ламинации
    work_laminate = 0
    if laminating[0] != 'без кашировки':
        result_laminat_lid = cardboard.get('lid_tray')[0]
        work_laminate += laminating_work(result_laminat_lid)
        result_laminat += result_laminat_lid
    if laminating[1] != 'без кашировки':
        result_laminat_tray = cardboard.get('lid_tray')[1]
        work_laminate += laminating_work(result_laminat_tray)
        result_laminat += result_laminat_tray
    # округление кашировки
    if result_laminat > 0:
        result_laminat = rou(result_laminat)

    # расчет изготовления в ручную крышка
    work_lid = folder_work(m2_folder)*m2_folder
    type_work_lid = 'Сборка крышки(папка) ручная.'
    shtamp_lid = resp_folder(a, b, c)

    if kol >= 500 and a >= 80 and b >= 65:
        if a <= 460 and b <= 380 and c >= 10 and c <= 120:
            # расчет изготовления на автоматической машине дна
            # расход бумаги дно
            paper_tray = paper.paper_tray_auto(mt_paper['lissiz'])
            result_paper_tray = paper_tray['Расход']
            # стоимость работы
            work_tray = machin_work_tray(paper_tray['m2'])
            type_work_tray = 'Сборка дна автомат.'
            # стоимость штампа
            shtamp_tray = resp_tray(a, b, c)*2
        else:
            # расчет изготовления вручную дна
            # расход материала
            paper_tray = paper.paper_tray_hand(mt_paper['lissiz'])
            result_paper_tray = paper_tray['Расход']
            # стоимость работы
            work_tray = (hand_work(a, b, c) * 0.66) * 0.7
            type_work_tray = 'Сборка дна ручная.'
            # стоимость штампа
            shtamp_tray = resp_tray(a, b, c)
    else:
        # расчет изготовления вручную дна
        # расход материала
        paper_tray = paper.paper_tray_hand(mt_paper['lissiz'])
        result_paper_tray = paper_tray['Расход']
        # стоимость работы
        work_tray = (hand_work(a, b, c) * 0.66) * 0.7
        type_work_tray = 'Сборка дна ручная.'
        # стоимость штампа
        shtamp_tray = resp_tray(a, b, c)

    # общая стоимость работы
    work = work_lid + work_tray + work_laminate

    shtamp_res = shtamp_lid + shtamp_tray

    # расход общий бумаги
    result_paper = float(rou(result_paper_lid + result_paper_tray))

    # информация
    info_cardboard_paper = {'Картон': cardboard.get("Информация"),
                            'Бумага': paper_lid.get("Информация") + paper_tray.get("Информация")}

    currency = {'euro': currency_req, 'rub': 1}

    # расчетные данные для калькуляции стоимости
    data_calc_hand = calc_count.objects.get(style_work='шкатулка магнитная ручная')
    data_calc_auto = calc_count.objects.get(style_work='лоток автомат')
    data_calc_lam = calc_count.objects.get(style_work='кашировка')
    all_data_calc = {
        'Сборка крышки(папка) ручная.': data_calc_hand,
        'Сборка дна ручная.': data_calc_hand,
        'Сборка дна автомат.': data_calc_auto,
        'кашировка': data_calc_lam,
    }
    # цена материала на коробку
    cardboard_price = cardboard_search_price(cardboard_req)
    paper_price_laminate_lid = material_price(laminating[0], kol, result_laminat_lid)
    paper_price_laminate_tray = material_price(laminating[1], kol, result_laminat_tray)

    # стоимость картона перемноженная на расход картона
    cardboard_count = (cardboard_price["price"] * (currency.get(cardboard_price["currency"])) * result_cardboard)

    # стоимость внутренней бумаги перемноженная на расход бумаги
    paper_count_laminate_lid = (paper_price_laminate_lid["price"]
                                * (currency.get(paper_price_laminate_lid["currency"])) * result_laminat_lid)
    paper_count_laminate_tray = (paper_price_laminate_tray["price"]
                                 * (currency.get(paper_price_laminate_tray["currency"])) * result_laminat_tray)

    # если кашировка печать и внешняя то добавляется в общюю расход
    if laminating[0] == 'Полноцветная печать 170 г/м2' and mt_paper['name'] == 'Полноцветная печать 170 г/м2':
        paper_count_laminate_lid = 0
        result_paper += result_laminat_lid
        paper_price_laminate_lid["material"] = 'Полноцветная печать 170 г/м2'
    else:
        paper_count_laminate_lid = paper_price_laminate_lid["price"]
    if laminating[1] == 'Полноцветная печать 170 г/м2' and mt_paper['name'] == 'Полноцветная печать 170 г/м2':
        paper_count_laminate_tray = 0
        result_paper += result_laminat_tray
        paper_price_laminate_tray["material"] = 'Полноцветная печать 170 г/м2'
    else:
        paper_count_laminate_tray = paper_price_laminate_tray["price"]

    # стоимость внешней бумаги перемноженная на расход бумаги
    result_paper = rou(result_paper)
    paper_price = material_price(paper_req, kol, rou(result_paper))
    if mt_paper['name'] == 'Полноцветная печать 170 г/м2':
        paper_count = paper_price["price"]
    else:
        paper_count = (paper_price["price"] * (currency.get(paper_price["currency"])) * result_paper)

    # непроизводственные перемноженные на стоимость работы
    nonproductworklid = work_lid * all_data_calc[type_work_lid].not_production
    nonproductworktray = work_tray * all_data_calc[type_work_tray].not_production
    nonproductworklaminating = work_laminate * data_calc_lam.not_production
    nonproductwork = nonproductworklid + nonproductworktray + nonproductworklaminating

    # запас на брак
    reject = max([all_data_calc[type_work_lid].reject, all_data_calc[type_work_tray].reject])
    # стоимость ручки
    handle_count = Material.objects.get(mt_name=handle).prise
    # магниты
    magnets = None
    if a > 0 and a <= 100:
        magnets = Material.objects.get(mt_name='Магниты 8х2').prise * 2
    elif a > 100 and a <= 350:
        magnets = Material.objects.get(mt_name='Магниты 8х2').prise * 4
    elif a > 350:
        magnets = Material.objects.get(mt_name='Магниты 8х2').prise * 6

    # подсчет всех производственных затрат
    production_cost = ((paper_count + cardboard_count + paper_count_laminate_lid + paper_count_laminate_tray)
                       * reject) + magnets + data_calc_hand.cut + work + nonproductwork
    # стоимости
    calc_sum = upper_cost(production_cost, uppercost)
    manager = proc_manager(production_cost + (shtamp_res / kol), uppercost, kol)

    data = {'Информация о коробке': f'Размер коробки {a}x{b}x{c}мм. Тираж {kol}шт. ',
            'Материал': mark_safe(f'Картон - {cardboard_req}. '
                                  f'Бумага внешняя - {paper_price["material"]}. '
                                  f'<br>Бумага внутреняя: дно - {paper_price_laminate_tray["material"]}. '),
            'Расходы': mark_safe(f'Расход картона - {toFixed(result_cardboard, 2)}л. '
                                 f'Расход бумаги внешней - {toFixed(result_paper, 2)}л. '
                                 f'<br>Расход бумаги внутренней: дно -  {toFixed(result_laminat_tray, 2)}л.'),
            'Информация картон': info_cardboard_paper['Картон'],
            'Информация бумага': info_cardboard_paper['Бумага'],
            'Работа': f'Стоимость работы: крышки(папка) - {int(work_lid)}руб., дно - {int(work_tray)}руб. '
                      f'внутренняя оклейка - {toFixed(work_laminate)} руб. {type_work_lid} {type_work_tray}',
            'Цены': prices_one(calc_sum, uppercost),
            'Цена заказа': count_all((calc_sum * kol) + shtamp_res),
            'Себек': f'Себестоимость заказа: {int((production_cost * kol) + manager["result"] + shtamp_res)} руб. ',
            'Маржа': marga_all(calc_sum * kol + shtamp_res, production_cost * kol + shtamp_res + manager['result']),
            'Процент менеджера': manager['информация'],
            'Цена штампа': f'Цена штампа - {toFixed(shtamp_res, 2)} руб.'}
    if show:
        print(f'оклейка непроизводственные - '
              f'\nкашировка непроизводственные - {data_calc_lam.not_production}'
              f'\nоклейка работа - '
              f'\nкашировка работа - {work_laminate}')
        print(
            '((стоимость бумаги + стоимость картона + кашировка крышки + кашировка дна) * % на брак)+ магниты + '
            'резчики + работа + непроизводственные')
        print(
            f'(({paper_count} + {cardboard_count} + {paper_count_laminate_lid} + {paper_count_laminate_tray}) * '
            f'{reject}) + {magnets} + {data_calc_hand.cut} + {work} + {nonproductwork}')
        print(data)

    return data

