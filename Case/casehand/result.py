from details.algprog.round import rou
from Case.casehand.calculate import ExpenceCase
from cub_box_0.models import calc_count
from details.algprog.toFix import toFixed
from services.marga import marga
from services.materialcalculate import material_information, material_price
from services.shtamp.case import resp_case
from services.shtamp.trayflap import resp_tray
from work.hand_work_cubbox import hand_work
from work.hand_work_laminating import laminating_work


def result_data_case_hand(a, b, c, cardboard_req, paper_req, currency_req, kol, laminating=None):
    # материал
    mt_cardboard = material_information(cardboard_req)
    mt_paper = material_information(paper_req)
    type_work = 'пенал ручной'
    obj_case = ExpenceCase(a, b, c, mt_cardboard["thickness"])
    cardboard = obj_case.result(mt_cardboard["lissiz"])['cardboard']
    paper = obj_case.result(mt_paper["lissiz"])['paper']

    # расход материала
    result_cardboard = rou(sum(cardboard.get('Расход')))
    result_paper = rou(paper.get('Расход'))
    result_laminat_case = cardboard.get('Расход')[0]
    result_laminat_tray = cardboard.get('Расход')[1]
    # округление кашировки
    if result_laminat_case > 0:
        result_laminat_case = rou(result_laminat_case)
    if result_laminat_tray > 0:
        result_laminat_tray = rou(result_laminat_tray)
    # информация
    info_cardboard_paper = {'Картон': cardboard.get("Информация"),
                            'Бумага': paper.get("Информация")}
    # стоимость работы
    work_case = hand_work(a, c, b)*0.75
    work_tray = hand_work(a, b, c)*0.66
    work_laminate = 0
    if laminating[0] != 'Без кашировки':
        work_laminate += laminating_work(cardboard.get('Расход')[0])
    if laminating[1] != 'Без кашировки':
        work_laminate += laminating_work(cardboard.get('Расход')[1])
    work = work_case + work_tray + work_laminate

    # стоимость штампа
    shtamp_case = resp_case(a, b, c)
    shtamp_tray = resp_tray(a, b, c)
    shtamp_res = shtamp_case+shtamp_tray
    currency = {'euro': currency_req, 'rub': 1}

    # расчетные данные для калькуляции стоимости
    data_calc = calc_count.objects.get(style_work=type_work)
    data_calc_lam = calc_count.objects.get(style_work='кашировка')
    # цена материала на коробку
    cardboard_price = material_price(cardboard_req, kol, result_cardboard)
    paper_price = material_price(paper_req, kol, result_paper)
    paper_price_laminate_case = material_price(laminating[0], kol, result_laminat_case)
    paper_price_laminate_tray = material_price(laminating[1], kol, result_laminat_tray)
    # стоимость картона перемноженная на расход картона
    cardboard_count = (cardboard_price["price"] * (currency.get(cardboard_price["currency"])) * result_cardboard)
    # стоимость внутренней бумаги перемноженная на расход бумаги
    paper_count_laminate_case = (paper_price_laminate_case["price"] * (currency.get(paper_price_laminate_case["currency"])) * result_laminat_case)
    paper_count_laminate_tray = (paper_price_laminate_tray["price"] * (currency.get(paper_price_laminate_tray["currency"])) * result_laminat_tray)
    if laminating[0] == 'Полноцветная печать 170 г/м2':
        paper_count_laminate_case = paper_price_laminate_case["price"]
    if laminating[1] == 'Полноцветная печать 170 г/м2':
        paper_count_laminate_tray = paper_price["price"]
    # стоимость внешней бумаги перемноженная на расход бумаги
    if mt_paper['name'] == 'Полноцветная печать 170 г/м2':
        paper_count = paper_price["price"]
    else:
        paper_count = (paper_price["price"] * (currency.get(paper_price["currency"])) * result_paper)
    # лента
    tape = 5
    # непроизводственные перемноженные на стоимость работы
    nonproductworklaminating = work_laminate * data_calc_lam.not_production
    nonproductwork = work * data_calc.not_production + nonproductworklaminating
    # подсчет всех производственных затрат
    production_cost = ((paper_count+cardboard_count+paper_count_laminate_case+paper_count_laminate_tray)*data_calc.reject)+tape+data_calc.cut+work+nonproductwork
    # стоимости
    calc_sum = marga(production_cost)

    data = {'Расход картона': result_cardboard,
            'Расход бумаги': result_paper,
            'Информация': info_cardboard_paper,
            'Работа': {'футляр': toFixed(work_case), 'лоток': toFixed(work_tray)},
            'Цены': calc_sum,
            'Цена штампа': float(toFixed(shtamp_res, 2))}
    return data

