from details.tray.trayhand.calculate import ExpenceTray
from cub_box_0.models import Material, calc_count
from details.algprog.currency import currency_eur as cur_euro
from details.tray.trayauto.shtamp import resp
from details.algprog.toFix import toFixed
from work.hand_work_cubbox import hand_work


def result_data_tray_hand(a, b, c, cardboard_req, paper_req):
    currency_req = cur_euro()
    thickness_cb = Material.objects.get(mt_name=cardboard_req).len
    lis_siz = [Material.objects.get(mt_name=cardboard_req).size_x, Material.objects.get(mt_name=cardboard_req).size_y]

    type_work = 'дно ручное'
    obj_tray = ExpenceTray(a, b, c, thickness_cb)
    result_cardboard = obj_tray.result(lis_siz).get('cardboard')
    result_paper = obj_tray.result(lis_siz).get('paper')
    work = (hand_work(a, b, c)/3)*2
    shtamp_res = resp(a, b, c)

    currency = {'euro': currency_req, 'rub': 1}
    data_calc = calc_count.objects.get(style_work=type_work)
    paper_obj = Material.objects.get(mt_name=paper_req)
    paper_count = (paper_obj.prise * (currency.get(paper_obj.currency))*result_paper.get('Расход'))
    cardboard_obj = Material.objects.get(mt_name= cardboard_req)
    cardboard_count = (cardboard_obj.prise * (currency.get(cardboard_obj.currency))*result_cardboard.get('Расход'))
    production_cost = (paper_count+cardboard_count)*data_calc.reject+data_calc.cut+work+((work)\
                                                                        *data_calc.not_production)
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
