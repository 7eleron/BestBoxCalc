from CasketM.casketauto.calculate import ExpenceCasket
from cub_box_0.models import Material, calc_count
from details.algprog.round import rou
from details.algprog.toFix import toFixed
from services.marga import marga
from services.shtamp.folderm import resp_folder
from services.shtamp.trayflap import resp_tray
from work.auto_work_tray import machin_work_tray
from work.hand_work_folder import folder_work


def result_data_casket_auto(a, b, c, cardboard_req, paper_req, cur_euro):
    currency_req = cur_euro
    # толщина картона
    thickness_cb = Material.objects.get(mt_name=cardboard_req).len
    # размер листа материала
    lissiz_cb = [Material.objects.get(mt_name=cardboard_req).size_x, Material.objects.get(mt_name=cardboard_req).size_y]
    lissiz_pap = [Material.objects.get(mt_name=paper_req).size_x, Material.objects.get(mt_name=paper_req).size_y]

    type_work = 'шкатулка магнитная полуавтомат'
    obj_casket = ExpenceCasket(a, b, c, thickness_cb)
    cardboard = obj_casket.result(lissiz_cb)['cardboard']
    paper = obj_casket.result(lissiz_pap)['paper']
    # расход материала
    result_cardboard = rou(cardboard.get('Расход'))
    result_paper = rou(paper.get('Расход'))
    # информация
    info_cardboard_paper = {'Картон': cardboard.get("Информация"),
                            'Бумага': paper.get("Информация")}

    m2_folder = paper['m2']['крышка']
    m2_tray = paper['m2']['дно']
    # стоимость работы
    work_fold = folder_work(m2_folder)*m2_folder
    work_tray = machin_work_tray(m2_tray)
    work = work_fold + work_tray
    # стоимость штампа
    shtamp_fold = resp_folder(a, b, c)
    shtamp_tray = resp_tray(a, b, c)*2
    shtamp_res = shtamp_fold + shtamp_tray

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
    # магниты
    magnets = None
    if a > 0 and a <= 100:
        magnets = Material.objects.get(mt_name='Магниты 8х2').prise * 2
    elif a > 100 and a <= 350:
        magnets = Material.objects.get(mt_name='Магниты 8х2').prise * 4
    elif a > 350:
        magnets = Material.objects.get(mt_name='Магниты 8х2').prise * 6

    # непроизводственные перемноженные на стоимость работы
    nonproductworkfold = work_fold * data_calc.not_production
    nonproductworktray = work_tray * data_calc_auto.not_production
    nonproductwork = nonproductworkfold + nonproductworktray
    # подсчет всех производственных затрат
    production_cost = ((paper_count+cardboard_count)*data_calc.reject)+magnets+data_calc.cut+work+nonproductwork
    # стоимости
    calc_sum = marga(production_cost)

    data = {'Расход картона': result_cardboard,
            'Расход бумаги': result_paper,
            'Информация': info_cardboard_paper,
            'Работа': {'папка': toFixed(work_fold), 'лоток': toFixed(work_tray)},
            'Цены': calc_sum,
            'Цена штампа': float(toFixed(shtamp_res, 2))}
    return data
