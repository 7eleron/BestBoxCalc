from cubbox.calculate import Cardboard_Box, Paper_Box_Hand, Paper_Box_Auto
from cub_box_0.models import Work, calc_count, Work2
from cubbox.shtamp import cutter
from details.algprog.round import rou
from details.algprog.toFix import toFixed
from services.marga import marga, prices
from services.materialcalculate import material_information, material_price
from work.hand_work_laminating import laminating_work


def machin_work(res_paper, kol):
    object_list = Work.objects.all()
    for obj in object_list:
        if obj.Name == 'крышка_авто' and obj.dm2 <= res_paper[0]:
            lid = ((obj.Content + obj.Scotch) + (obj.Close_fitting / kol)) + obj.Lid
        elif obj.Name == 'дно_авто' and obj.dm2 <= res_paper[1]:
            tray = ((obj.Content + obj.Scotch) + (obj.Close_fitting / kol)) + obj.Tray
    return [lid, tray]


def hand_work(a, b, hight):
    object_list = Work2.objects.all()
    size_box = a+b
    work_count = None
    for obj in object_list:
        if size_box <= obj.Size and hight <= obj.Hight:
            work_count = obj.Count
            break
    return work_count


def result_data_box(a, b, c, cardboard_req, paper_req, kol, lid_hight, currency_req, laminating):
    # материал
    mt_cardboard = material_information(cardboard_req)
    mt_paper = material_information(paper_req)

    if kol >= 500 and a >= 80 and b >= 65 and c >= 10:
        # расчет изготовления на автоматической машине
        if a <= 460 and b <= 380 and c <= 120:
            cardboard = Cardboard_Box(a, b, c, mt_cardboard["thickness"], lid_hight).cardboard_box(lis_siz=mt_cardboard["lissiz"])
            paper = Paper_Box_Auto(a, b, c, mt_cardboard["thickness"], lid_hight).cub_box_paper(lis_siz=mt_paper["lissiz"])
            # расход материала
            result_cardboard = cardboard['Расход']
            result_paper = paper['Расход']
            result_laminat_lid = cardboard.get('lid_tray')[0]
            result_laminat_tray = cardboard.get('lid_tray')[1]
            # округление кашировки
            if result_laminat_lid > 0:
                result_laminat_lid = rou(result_laminat_lid)
            if result_laminat_tray > 0:
                result_laminat_tray = rou(result_laminat_tray)
            # информация
            info_cardboard_paper = {'Картон': cardboard.get("Информация"),
                                    'Бумага': paper.get("Информация")}
            lid = machin_work(paper['m2'], kol)[0]
            tray = machin_work(paper['m2'], kol)[1]
            # стоимость работы
            work_laminate = 0
            if laminating[0] != 'Без кашировки':
                work_laminate += laminating_work(cardboard.get('lid_tray')[0])
            if laminating[1] != 'Без кашировки':
                work_laminate += laminating_work(cardboard.get('lid_tray')[1])
            worklidtray = lid + tray
            work = worklidtray + work_laminate
            type_work = ['Сборка автоматическая.', 'кд автомат']
            # стоимость штампа
            shtamp_res = cutter(a, b, c, lid_hight)*2

        # расчет изготовления лотка вручную
        else:
            cardboard = Cardboard_Box(a, b, c, mt_cardboard["thickness"], lid_hight).cardboard_box(
                lis_siz=mt_cardboard["lissiz"])
            paper = Paper_Box_Hand(a, b, c, mt_cardboard["thickness"], lid_hight).cub_box_paper(
                lis_siz=mt_paper["lissiz"])
            # расход материала
            result_cardboard = cardboard['Расход']
            result_paper = paper['Расход']
            result_laminat_lid = cardboard.get('lid_tray')[0]
            result_laminat_tray = cardboard.get('lid_tray')[1]
            # округление кашировки
            if result_laminat_lid > 0:
                result_laminat_lid = rou(result_laminat_lid)
            if result_laminat_tray > 0:
                result_laminat_tray = rou(result_laminat_tray)
            # информация
            info_cardboard_paper = {'Картон': cardboard.get("Информация"),
                                    'Бумага': paper.get("Информация")}
            # стоимость работы
            work_laminate = 0
            if laminating[0] != 'Без кашировки':
                work_laminate += laminating_work(cardboard.get('lid_tray')[0])
            if laminating[1] != 'Без кашировки':
                work_laminate += laminating_work(cardboard.get('lid_tray')[1])
            worklidtray = hand_work(a, b, c)
            work = worklidtray + work_laminate
            type_work = ['Сборка ручная.', 'кд ручное']
            # стоимость штампа
            shtamp_res = cutter(a, b, c, lid_hight)

    # расчет изготовления лотка вручную
    else:
        cardboard = Cardboard_Box(a, b, c, mt_cardboard["thickness"], lid_hight).cardboard_box(
            lis_siz=mt_cardboard["lissiz"])
        paper = Paper_Box_Hand(a, b, c, mt_cardboard["thickness"], lid_hight).cub_box_paper(
            lis_siz=mt_paper["lissiz"])
        # расход материала
        result_cardboard = cardboard['Расход']
        result_paper = paper['Расход']
        result_laminat_lid = cardboard.get('lid_tray')[0]
        result_laminat_tray = cardboard.get('lid_tray')[1]
        # округление кашировки
        if result_laminat_lid > 0:
            result_laminat_lid = rou(result_laminat_lid)
        if result_laminat_tray > 0:
            result_laminat_tray = rou(result_laminat_tray)
        # информация
        info_cardboard_paper = {'Картон': cardboard.get("Информация"),
                                'Бумага': paper.get("Информация")}
        # стоимость работы
        work_laminate = 0
        if laminating[0] != 'Без кашировки':
            work_laminate += laminating_work(cardboard.get('lid_tray')[0])
        if laminating[1] != 'Без кашировки':
            work_laminate += laminating_work(cardboard.get('lid_tray')[1])
        worklidtray = hand_work(a, b, c)
        work = worklidtray + work_laminate
        type_work = ['Сборка ручная.', 'кд ручное']
        # стоимость штампа
        shtamp_res = cutter(a, b, c, lid_hight)
    currency = {'euro': currency_req, 'rub': 1}
    # расчетные данные для калькуляции стоимости
    data_calc = calc_count.objects.get(style_work=type_work[1])
    data_calc_lam = calc_count.objects.get(style_work='кашировка')
    # цена материала на коробку
    cardboard_price = material_price(cardboard_req, kol, result_cardboard)
    paper_price = material_price(paper_req, kol, result_paper)
    paper_price_laminate_lid = material_price(laminating[0], kol, result_laminat_lid)
    paper_price_laminate_tray = material_price(laminating[1], kol, result_laminat_tray)
    # стоимость картона перемноженная на расход картона
    cardboard_count = (cardboard_price["price"] * (currency.get(cardboard_price["currency"])) * result_cardboard)
    # стоимость внутренней бумаги перемноженная на расход бумаги
    paper_count_laminate_lid = (paper_price_laminate_lid["price"] * (currency.get(paper_price_laminate_lid["currency"])) * result_laminat_lid)
    paper_count_laminate_tray = (paper_price_laminate_tray["price"] * (currency.get(paper_price_laminate_tray["currency"])) * result_laminat_tray)
    if laminating[0] == 'Полноцветная печать 170 г/м2':
        paper_count_laminate_lid = paper_price_laminate_lid["price"]
    if laminating[1] == 'Полноцветная печать 170 г/м2':
        paper_count_laminate_tray = paper_price["price"]
    # стоимость внешней бумаги перемноженная на расход бумаги
    if mt_paper['name'] == 'Полноцветная печать 170 г/м2':
        paper_count = paper_price["price"]
    else:
        paper_count = (paper_price["price"] * (currency.get(paper_price["currency"])) * result_paper)
    # непроизводственные перемноженные на стоимость работы
    nonproductworklidtray = worklidtray * data_calc.not_production
    nonproductworklaminating = work_laminate * data_calc_lam.not_production
    nonproductwork = nonproductworklidtray + nonproductworklaminating
    # подсчет всех производственных затрат
    production_cost = ((paper_count+cardboard_count+paper_count_laminate_lid+paper_count_laminate_tray)*data_calc.reject)+data_calc.cut+work+nonproductwork
    # стоимости
    calc_sum = marga(production_cost)

    data = {'Информация о коробке': f'Размер коробки {a}x{b}x{c}мм. Высота крышки {lid_hight}. Тираж {kol}шт. '
                                    f'Картон - {cardboard_req}. Бумага - {paper_req}. ',
            'Расходы': f'Расход картона - {toFixed(result_cardboard, 2)}л. Расход бумаги - {toFixed(result_paper, 2)}л. ',
            'Информация картон': info_cardboard_paper['Картон'],
            'Информация бумага': info_cardboard_paper['Бумага'],
            'Работа': f'Стоимость работы - {work} руб. {type_work[0]}',
            'Цены': prices(calc_sum),
            'Цена штампа': f'Цена штампа - {toFixed(shtamp_res, 2)} руб.'}
    print(data)
    return data
