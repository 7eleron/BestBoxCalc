from details.algprog.round import rou
from CubBoxInsert.cubboxinsert.cbinsertauto.calculate import ExpenceCubBoxInsert
from cub_box_0.models import Material, calc_count
from details.algprog.toFix import toFixed
from services.marga import marga
from services.materialcalculate import material_information, material_price
from services.shtamp.cdinsert import resp_insert
from work.auto_work_tray import machin_work_tray
from work.hand_work_laminating import laminating_work


def result_data_cdinsert_auto(a, b, tray_hight, lid_hight, insert_hight, cardboard_req, paper_req, currency_req, kol, laminating=None):
    # материал
    mt_cardboard = material_information(cardboard_req)
    mt_paper = material_information(paper_req)
    type_work = 'кд с вставкой автомат'
    obj_cbinsert = ExpenceCubBoxInsert(a, b, tray_hight, lid_hight, insert_hight, mt_cardboard["thickness"])
    cardboard = obj_cbinsert.result(mt_cardboard["lissiz"])['cardboard']
    paper = obj_cbinsert.result(mt_paper["lissiz"])['paper']

    # расход материала
    result_cardboard = rou(sum(cardboard.get('Расход')))
    result_paper = rou(paper.get('Расход'))
    result_laminat_lid = cardboard.get('Расход')[0]
    result_laminat_insert = cardboard.get('Расход')[2]
    # округление кашировки
    if result_laminat_lid > 0:
        result_laminat_lid = rou(result_laminat_lid)
    if result_laminat_insert > 0:
        result_laminat_insert = rou(result_laminat_insert)
    # информация
    info_cardboard_paper = {'Картон': cardboard.get("Информация"),
                            'Бумага': paper.get("Информация")}
    # стоимость работы
    work_laminate = 0
    if laminating[0] != 'Без кашировки':
        work_laminate += laminating_work(cardboard.get('Расход')[0])
    if laminating[1] != 'Без кашировки':
        work_laminate += laminating_work(cardboard.get('Расход')[2])
    worklidinserttray = machin_work_tray(paper['m2']['крышка']) + \
                        machin_work_tray(paper['m2']['дно']) + \
                        machin_work_tray(paper['m2']['вставка'])
    work = worklidinserttray + work_laminate
    # стоимость штампа
    shtamp_res = resp_insert(a, b, tray_hight, lid_hight, insert_hight)*1.66

    currency = {'euro': currency_req, 'rub': 1}
    # расчетные данные для калькуляции стоимости
    data_calc = calc_count.objects.get(style_work=type_work)
    data_calc_lam = calc_count.objects.get(style_work='кашировка')
    # цена материала на коробку
    cardboard_price = material_price(cardboard_req, kol, result_cardboard)
    paper_price = material_price(paper_req, kol, result_paper)
    paper_price_laminate_lid = material_price(laminating[0], kol, result_laminat_lid)
    paper_price_laminate_insert = material_price(laminating[1], kol, result_laminat_insert)
    # стоимость картона перемноженная на расход картона
    cardboard_count = (cardboard_price["price"] * (currency.get(cardboard_price["currency"])) * result_cardboard)
    # стоимость внутренней бумаги перемноженная на расход бумаги
    paper_count_laminate_lid = (paper_price_laminate_lid["price"] * (
        currency.get(paper_price_laminate_lid["currency"])) * result_laminat_lid)
    paper_count_laminate_insert = (paper_price_laminate_insert["price"] * (
        currency.get(paper_price_laminate_insert["currency"])) * result_laminat_insert)
    if laminating[0] == 'Полноцветная печать 170 г/м2':
        paper_count_laminate_lid = paper_price_laminate_lid["price"]
    if laminating[1] == 'Полноцветная печать 170 г/м2':
        paper_count_laminate_insert = paper_price["price"]
    # стоимость внешней бумаги перемноженная на расход бумаги
    if mt_paper['name'] == 'Полноцветная печать 170 г/м2':
        paper_count = paper_price["price"]
    else:
        paper_count = (paper_price["price"] * (currency.get(paper_price["currency"])) * result_paper)
    # клей для всавки
    glue = 5
    # непроизводственные перемноженные на стоимость работы
    nonproductworklaminating = work_laminate * data_calc_lam.not_production
    nonproductworklidinserttray = worklidinserttray * data_calc.not_production
    nonproductwork = nonproductworklidinserttray + nonproductworklaminating
    # подсчет всех производственных затрат
    production_cost = ((paper_count+cardboard_count+paper_count_laminate_lid+paper_count_laminate_insert)*data_calc.reject)+glue+data_calc.cut+work+nonproductwork
    # стоимости
    calc_sum = marga(production_cost)

    data = {'Расход картона': result_cardboard,
            'Расход бумаги': result_paper,
            'Информация': info_cardboard_paper,
            'Работа': float(toFixed(work, 2)),
            'Цены': calc_sum,
            'Цена штампа': toFixed(shtamp_res, 2)}
    return data
