from details.lid.lidhand.calculate import ExpenceLid
from cub_box_0.models import Material, calc_count
from details.algprog.currency import currency_eur as cur_euro
from details.tray.trayauto.shtamp import resp
from details.algprog.toFix import toFixed
from work.hand_work_cubbox import hand_work


def result_data_lid_hand(a, b, c, cardboard_req, paper_req, currency_req):
    # толщина картона
    thickness_cb = Material.objects.get(mt_name=cardboard_req).len
    # размер листа материала
    lissiz_cb = [Material.objects.get(mt_name=cardboard_req).size_x, Material.objects.get(mt_name=cardboard_req).size_y]
    lissiz_pap = [Material.objects.get(mt_name=paper_req).size_x, Material.objects.get(mt_name=paper_req).size_y]

    type_work = 'крышка ручная'
    # расход материала
    obj_tray = ExpenceLid(a, b, c, thickness_cb)
    result_cardboard = obj_tray.result(lissiz_cb)['cardboard'].get('Расход')
    result_paper = obj_tray.result(lissiz_pap)['paper'].get('Расход')
    # стоимость работы
    work = hand_work(a, b, c)/3
    # стоимость штампа
    shtamp_res = resp(a, b, c)

    currency = {'euro': currency_req, 'rub': 1}
    # расчетные данные для калькуляции стоимости
    data_calc = calc_count.objects.get(style_work=type_work)
    # материал
    paper_obj = Material.objects.get(mt_name=paper_req)
    cardboard_obj = Material.objects.get(mt_name= cardboard_req)
    # стоимость бумаги перемноженная на расход бумаги
    paper_count = (paper_obj.prise * (currency.get(paper_obj.currency))*result_paper.get('Расход'))
    # стоимость картона перемноженная на расход картона
    cardboard_count = (cardboard_obj.prise * (currency.get(cardboard_obj.currency))*result_cardboard.get('Расход'))
    # подсчет всех производственных затрат
    production_cost = (paper_count+cardboard_count)*data_calc.reject+data_calc.cut+work+((work)\
                                                                        *data_calc.not_production)
    # стоимости
    calc_sum = ((production_cost*data_calc.margin)*data_calc.manager_proc)+production_cost

    data = {'Расход картона': result_cardboard.get('Расход'),
            'Расход бумаги': result_paper.get("Расход"),
            'Информация картон': result_cardboard.get("Информация"),
            'Информация бумага': result_paper.get("Информация"),
            'Работа': float(toFixed(work, 2)),
            'Cборка': type_work,
            'Цена лотка': toFixed(calc_sum, 2),
            'Цена штампа': float(toFixed(shtamp_res, 2))}
    return data
