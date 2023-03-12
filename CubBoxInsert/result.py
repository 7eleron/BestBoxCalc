from django.utils.safestring import mark_safe

from CubBoxInsert.cubboxinsert.calculate import CardboardCubBoxInsert, PaperBoxInsert
from cub_box_0.models import calc_count
from details.algprog.round import rou
from details.algprog.toFix import toFixed
from services.marga import prices_one, upper_cost, count_all, marga_all, proc_manager
from services.materialcalculate import material_information, material_price, cardboard_search_price
from services.showdetailcalc import show
from services.shtamp.cdinsert import resp_insert
from services.shtamp.mold import mold
from work.auto_work_tray import machin_work_tray
from work.hand_work_cubbox import hand_work
from work.hand_work_laminating import laminating_work


def result_data_cdinsert(a, b, tray_hight, insert_hight, cardboard_req, paper_req, kol, lid_hight,
                         currency_req, laminating, uppercost, feature):
    # материал
    mt_cardboard = material_information(cardboard_req)
    mt_paper = material_information(paper_req)
    cardboard = CardboardCubBoxInsert(width=a, length=b, tray_hight=tray_hight, lid_hight=lid_hight,
                                      insert_hight=insert_hight, thickness_cb=mt_cardboard["thickness"]
                                      ).cardboard_box(lis_siz=mt_cardboard["lissiz"])
    paper = PaperBoxInsert(width=a, length=b, tray_hight=tray_hight, lid_hight=lid_hight, insert_hight=insert_hight,
                           thickness_cb=mt_cardboard["thickness"])
    # расход картона
    result_cardboard = cardboard['Расход']
    # расход бумаги, крышка
    paper_lid = paper.lid(mt_paper['lissiz'])
    result_paper_lid = paper_lid['Расход']
    # расход бумаги, вкаставка
    paper_insert = paper.insert(mt_paper['lissiz'])
    result_paper_insert = paper_insert['Расход']

    # кашировка
    result_laminat_lid = 0
    result_laminat_insert = 0
    result_laminat = 0
    # стоимость работы ламинации
    work_laminate = 0
    if laminating[0] != 'без кашировки':
        result_laminat_lid = cardboard.get('lid_tray_insert')[0]
        work_laminate += laminating_work(result_laminat_lid)
        result_laminat += result_laminat_lid
    if laminating[1] != 'без кашировки':
        result_laminat_insert = cardboard.get('lid_tray_insert')[2]
        work_laminate += laminating_work(result_laminat_insert)
        result_laminat += result_laminat_insert
    # округление кашировки
    if result_laminat > 0:
        result_laminat = rou(result_laminat)

    shtamp_res = 0

    if kol >= 500 and a >= 60 and b >= 60:
        if a <= 460 and b <= 380 and lid_hight >= 10 and lid_hight <= 120:
            # расчет изготовления на автоматической машине крышка
            work_lid = machin_work_tray(paper_lid['m2'])
            type_work_lid = 'Сборка крышки автомат.'
            shtamp_res += resp_insert(a, b, tray_hight, lid_hight, insert_hight) * 0.5
        else:
            # расчет изготовления в ручную крышка
            work_lid = hand_work(a, b, tray_hight) * 0.33
            type_work_lid = 'Сборка крышки ручная.'

        if a <= 460 and b <= 380 and insert_hight >= 10 and insert_hight <= 120:
            # расчет изготовления на автоматической машине вставка
            work_insert = machin_work_tray(paper_insert['m2'])
            type_work_insert = 'Сборка вставки автомат.'
            shtamp_res += resp_insert(a, b, tray_hight, lid_hight, insert_hight) * 0.5 + mold(a, b, insert_hight)
        else:
            # расчет изготовления вручную вставка
            work_insert = hand_work(a, b, insert_hight) * 0.66
            type_work_insert = 'Сборка вставки ручная.'

        if a <= 460 and b <= 380 and tray_hight >= 10 and tray_hight <= 120:
            # расчет изготовления на автоматической машине дно
            # расход бумаги дно
            paper_tray = paper.paper_tray_auto(mt_paper['lissiz'])
            result_paper_tray = paper_tray['Расход']
            # стоимость работы
            work_tray = machin_work_tray(paper_tray['m2'])
            type_work_tray = 'Сборка дна автомат.'
            # стоимость штампа
            shtamp_res += resp_insert(a, b, tray_hight, lid_hight, insert_hight) * 1.5 + mold(a, b, tray_hight)
        else:
            # расчет изготовления вручную дно
            # расход бумаги дно
            paper_tray = paper.paper_tray_hand(mt_paper['lissiz'])
            result_paper_tray = paper_tray['Расход']
            # стоимость работы
            work_tray = hand_work(a, b, tray_hight) * 0.66
            type_work_tray = 'Сборка дна ручная.'
            # стоимость штампа
            shtamp_res = resp_insert(a, b, tray_hight, lid_hight, insert_hight)

    else:
        # расчет изготовления крышка, дно, вставка вручную
        # стоимость работы
        work_lid = hand_work(a, b, tray_hight) * 0.33
        work_tray = hand_work(a, b, tray_hight) * 0.66
        work_insert = hand_work(a, b, insert_hight) * 0.66
        type_work_lid = 'Сборка крышки ручная.'
        type_work_tray = 'Сборка дна ручная.'
        type_work_insert = 'Сборка вставки ручная.'
        # расход материала
        paper_tray = paper.paper_tray_hand(mt_paper['lissiz'])
        result_paper_tray = paper_tray['Расход']
        # стоимость штампа
        shtamp_res = resp_insert(a, b, tray_hight, lid_hight, insert_hight)

    # общая стоимость работы
    work = work_lid + work_insert + work_tray + work_laminate

    # расход общий бумаги
    result_paper = float(rou(result_paper_lid + result_paper_tray + result_paper_insert))

    # информация
    info_cardboard_paper = {'Картон': cardboard.get("Информация"),
                            'Бумага': paper_lid.get("Информация") + paper_tray.get("Информация") +
                                      paper_insert.get("Информация")}

    currency = {'euro': currency_req, 'rub': 1}

    # расчетные данные для калькуляции стоимости
    data_calc_hand = calc_count.objects.get(style_work='кд с вставкой ручной')
    data_calc_auto = calc_count.objects.get(style_work='кд с вставкой автомат')
    data_calc_lam = calc_count.objects.get(style_work='кашировка')
    all_data_calc = {
        'Сборка крышки ручная.': data_calc_hand,
        'Сборка крышки автомат.': data_calc_auto,
        'Сборка дна ручная.': data_calc_hand,
        'Сборка дна автомат.': data_calc_auto,
        'Сборка вставки ручная.': data_calc_hand,
        'Сборка вставки автомат.': data_calc_auto,
        'кашировка': data_calc_lam,
    }
    # цена материала на коробку
    cardboard_price = cardboard_search_price(cardboard_req)
    paper_price_laminate_lid = material_price(laminating[0], kol, result_laminat_lid)
    paper_price_laminate_insert = material_price(laminating[1], kol, result_laminat_insert)
    # стоимость картона перемноженная на расход картона
    cardboard_count = (cardboard_price["price"] * (currency.get(cardboard_price["currency"])) * result_cardboard)

    # стоимость внутренней бумаги перемноженная на расход бумаги
    paper_count_laminate_lid = (paper_price_laminate_lid["price"]
                                * (currency.get(paper_price_laminate_lid["currency"])) * result_laminat_lid)
    paper_count_laminate_insert = (paper_price_laminate_insert["price"]
                                   * (currency.get(paper_price_laminate_insert["currency"])) * result_laminat_insert)

    # если кашировка печать и внешняя то добавляется в общюю расход
    if laminating[0] == 'Полноцветная печать 170 г/м2' and mt_paper['name'] == 'Полноцветная печать 170 г/м2':
        paper_count_laminate_lid = 0
        result_paper += result_laminat_lid
        paper_price_laminate_lid["material"] = 'Полноцветная печать 170 г/м2'
    else:
        paper_count_laminate_lid = paper_price_laminate_lid["price"]
    if laminating[1] == 'Полноцветная печать 170 г/м2' and mt_paper['name'] == 'Полноцветная печать 170 г/м2':
        paper_count_laminate_insert = 0
        result_paper += result_laminat_insert
        paper_price_laminate_insert["material"] = 'Полноцветная печать 170 г/м2'
    else:
        paper_count_laminate_insert = paper_price_laminate_insert["price"]

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
    nonproductworkinsert = work_insert * all_data_calc[type_work_insert].not_production
    nonproductworklaminating = work_laminate * data_calc_lam.not_production
    nonproductwork = nonproductworklid + nonproductworktray + nonproductworkinsert + nonproductworklaminating

    # запас на брак
    reject = max([all_data_calc[type_work_lid].reject, all_data_calc[type_work_tray].reject,
                  all_data_calc[type_work_insert].reject])

    # клей для всавки
    glue = 5

    # подсчет всех производственных затрат
    production_cost = ((paper_count + cardboard_count + paper_count_laminate_lid + paper_count_laminate_insert)
                       * reject) + glue + data_calc_hand.cut + work + nonproductwork

    # стоимости
    calc_sum = upper_cost(production_cost, uppercost)
    manager = proc_manager(production_cost + (shtamp_res / kol), uppercost, kol)

    if tray_hight+lid_hight >= insert_hight:
        all_hight = tray_hight+lid_hight
    else:
        all_hight = insert_hight

    # доп услуги
    # тиснение наценка
    pressfoil_one = feature['pressfoil'] / kol

    # шелкография наценка
    pattern_one = feature['pattern'] / kol

    # ложементы наценка
    logement_one = feature['logement'] / kol

    data = {'Информация о коробке': f'Размер коробки {a}x{b}x{all_hight}мм. '
                                    f'Крышка {lid_hight}мм, дно {tray_hight}мм, вставка {insert_hight}мм. Тираж {kol}шт. ',
            'Материал': mark_safe(f'Картон - {cardboard_req}. '
                                  f'Бумага внешняя - {paper_price["material"]}. '
                                  f'<br>Бумага внутреняя: крышка - {paper_price_laminate_lid["material"]}; '
                                  f'дно - {paper_price_laminate_insert["material"]}. '),
            'Расходы': mark_safe(f'Расход картона - {toFixed(result_cardboard, 2)}л. '
                                 f'Расход бумаги внешней - {toFixed(result_paper, 2)}л. '
                                 f'<br>Расход бумаги внутренней: крышка - {toFixed(result_laminat_lid, 2)}л.; '
                                 f'дно -  {toFixed(result_laminat_insert, 2)}л.'),
            'Информация картон': info_cardboard_paper['Картон'],
            'Информация бумага': info_cardboard_paper['Бумага'],
            'Работа': f'Стоимость работы: крышка - {toFixed(work_lid)} руб., дно - {toFixed(work_tray)} руб., '
                      f'внутренняя оклейка - {toFixed(work_laminate)} руб. {type_work_lid} {type_work_tray} ',
            'Цены': prices_one(calc_sum + pressfoil_one + pattern_one + logement_one, uppercost),
            'Цена заказа': count_all((calc_sum * kol) + shtamp_res +
                                     feature['pressfoil'] + feature['pattern'] + feature['logement']),
            'Себек': f'Себестоимость заказа: {int((production_cost * kol) + manager["result"] + shtamp_res)} руб. ',
            'Маржа': marga_all(calc_sum * kol + shtamp_res, production_cost * kol + shtamp_res + manager['result']),
            'Процент менеджера': manager['информация'],
            'Цена штампа': f'Цена штампа - {toFixed(shtamp_res, 2)} руб.'}

    if show:
        print(f'оклейка непроизводственные - '
              f'\nкашировка непроизводственные - {data_calc_lam.not_production}'
              f'\nоклейка работа - '
              f'\nкашировка работа - {work_laminate}')
        print('((стоимость бумаги + стоимость картона + кашировка крышки + кашировка вставка) * % на брак)+ клей '
              '+ резчики + работа + непроизводственные')
        print(
            f'(({paper_count} + {cardboard_count} + {paper_count_laminate_lid} + {paper_count_laminate_insert}) '
            f'* {reject}) + {glue} + {data_calc_hand.cut} + {work} + {nonproductwork}')
        print(data)
    return data

