from details.algprog.round import rou
from Case.caseauto.calculate import ExpenceCase
from cub_box_0.models import Material, calc_count
from details.algprog.toFix import toFixed
from services.marga import marga
from services.shtamp.case import resp_case
from services.shtamp.trayflap import resp_tray
from work.auto_work_tray import machin_work_tray
from work.hand_work_cubbox import hand_work


def result_data_case_auto(a, b, c, cardboard_req, paper_req, currency_req):
    # толщина картона
    thickness_cb = Material.objects.get(mt_name=cardboard_req).len
    # размер листа материала
    lissiz_cb = [Material.objects.get(mt_name=cardboard_req).size_x, Material.objects.get(mt_name=cardboard_req).size_y]
    lissiz_pap = [Material.objects.get(mt_name=paper_req).size_x, Material.objects.get(mt_name=paper_req).size_y]

    type_work = 'пенал полуавтомат'
    obj_case = ExpenceCase(a, b, c, thickness_cb)
    cardboard = obj_case.result(lissiz_cb)['cardboard']
    paper = obj_case.result(lissiz_pap)['paper']
    # расход материала
    result_cardboard = rou(cardboard.get('Расход'))
    result_paper = rou(paper.get('Расход'))
    # информация
    info_cardboard_paper = {'Картон': cardboard.get("Информация"),
                            'Бумага': paper.get("Информация")}
    # стоимость работы
    work_case = hand_work(a, c, b)*0.75
    work_tray = machin_work_tray(paper['m2']['дно'])
    work = work_case+work_tray

    # стоимость штампа
    shtamp_case = resp_case(a, b, c)
    shtamp_tray = resp_tray(a, b, c)*2
    shtamp_res = shtamp_case+shtamp_tray

    currency = {'euro': currency_req, 'rub': 1}
    # расчетные данные для калькуляции стоимости
    data_calc = calc_count.objects.get(style_work=type_work)
    data_calc_auto = calc_count.objects.get(style_work='лоток автомат')
    # материал
    cardboard_obj = Material.objects.get(mt_name=cardboard_req)
    paper_obj = Material.objects.get(mt_name=paper_req)
    # стоимость бумаги перемноженная на расход бумаги
    paper_count = (paper_obj.prise * (currency.get(paper_obj.currency))*result_paper)
    # стоимость картона перемноженная на расход картона
    cardboard_count = (cardboard_obj.prise * (currency.get(cardboard_obj.currency))*result_cardboard)
    # лента
    tape = 5
    # непроизводственные перемноженные на стоимость работы
    nonproductworkcase = work_case * data_calc.not_production
    nonproductworktray = work_tray * data_calc_auto.not_production
    nonproductwork = nonproductworkcase + nonproductworktray
    # подсчет всех производственных затрат
    production_cost = ((paper_count+cardboard_count)*data_calc.reject)+tape+data_calc.cut+work+nonproductwork
    # стоимости
    calc_sum = marga(production_cost)

    data = {'Расход картона': result_cardboard,
            'Расход бумаги': result_paper,
            'Информация': info_cardboard_paper,
            'Работа': {'футляр': toFixed(work_case), 'лоток': toFixed(work_tray)},
            'Цены': calc_sum,
            'Цена штампа': float(toFixed(shtamp_res, 2))}
    return data

