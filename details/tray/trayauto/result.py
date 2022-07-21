from details.tray.trayauto.calculate import ExpenceTray
from cub_box_0.models import Material, calc_count
from details.algprog.currency import currency_eur as cur_euro
from details.tray.trayauto.shtamp import resp
from details.algprog.toFix import toFixed
from work.auto_work_tray import machin_work_tray


def result_data_tray_auto(a, b, c, cardboard_req, paper_req):
    currency_req = cur_euro()
    thickness_cb = Material.objects.get(mt_name=cardboard_req).len
    lis_siz = [Material.objects.get(mt_name=cardboard_req).size_x, Material.objects.get(mt_name=cardboard_req).size_y]

    type_work = 'лоток автомат'
    obj_tray = ExpenceTray(a, b, c, thickness_cb)
    result_cardboard = obj_tray.result(lis_siz).get('cardboard')
    result_paper = obj_tray.result(lis_siz).get('paper')
    work = machin_work_tray(result_paper.get('m2'))
    shtamp_res = resp(a, b, c)

    currency = {'euro': currency_req, 'rub': 1}
    data_calc = calc_count.objects.get(style_work=type_work)
    paper_obj = Material.objects.get(mt_name=paper_req)
    paper_count = (paper_obj.prise * (currency.get(paper_obj.currency))*result_paper.get('Расход'))
    cardboard_obj = Material.objects.get(mt_name=cardboard_req)
    cardboard_count = (cardboard_obj.prise * (currency.get(cardboard_obj.currency))*result_cardboard.get('Расход'))
    production_cost = (paper_count+cardboard_count)*data_calc.reject+data_calc.cut+work+((work)\
                                                                        *data_calc.not_production)
    calc_sum = [((production_cost * 0.4) * data_calc.manager_proc) + production_cost,
                ((production_cost * 0.5) * data_calc.manager_proc) + production_cost,
                ((production_cost * 0.6) * data_calc.manager_proc) + production_cost,
                ((production_cost * 0.7) * data_calc.manager_proc) + production_cost,
                ((production_cost * 0.8) * data_calc.manager_proc) + production_cost,
                ((production_cost * 0.9) * data_calc.manager_proc) + production_cost,
                ((production_cost * 1) * data_calc.manager_proc) + production_cost
                ]
    data = {'Расход картона': result_cardboard.get('Расход'),
            'Расход бумаги': result_paper.get("Расход"),
            'Работа': float(toFixed(work, 2)),
            'Цена': calc_sum,
            'Цена лотка': f'Цена лотка: 40% - {toFixed(calc_sum[0], 2)} руб/шт. '
                          f'50% - {toFixed(calc_sum[1], 2)} руб/шт. '
                          f'60% - {toFixed(calc_sum[2], 2)} руб/шт. '
                          f'70% - {toFixed(calc_sum[3], 2)} руб/шт. '
                          f'80% - {toFixed(calc_sum[4], 2)} руб/шт. '
                          f'90% - {toFixed(calc_sum[5], 2)} руб/шт. '
                          f'100% - {toFixed(calc_sum[6], 2)} руб/шт. ',
            'Цена штампа': float(toFixed(shtamp_res, 2))*2}
    return data