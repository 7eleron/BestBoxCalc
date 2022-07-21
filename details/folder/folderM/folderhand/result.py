from details.folder.folderM.folderhand.calculate import ExpenceFolder
from cub_box_0.models import Material, calc_count
from details.algprog.currency import currency_eur as cur_euro
from details.folder.folderM.folderhand.shtamp import resp
from details.algprog.toFix import toFixed
from work.hand_work_folder import folder_work


def result_data_folder_hand(a, b, c, cardboard_req, paper_req):
    currency_req = cur_euro()
    thickness_cb = Material.objects.get(mt_name=cardboard_req).len
    lis_siz = [Material.objects.get(mt_name=cardboard_req).size_x, Material.objects.get(mt_name=cardboard_req).size_y]

    type_work = 'папка магниты ручная'
    obj_tray = ExpenceFolder(a, b, c, thickness_cb)
    result_cardboard = obj_tray.result(lis_siz).get('cardboard')
    result_paper_fold = obj_tray.result(lis_siz).get('paper_folder')
    result_paper_end = obj_tray.result(lis_siz).get('paper_end')
    result_paper = result_paper_fold.get('Расход')+result_paper_end.get('Расход')
    work = folder_work(result_paper_fold.get('m2')+result_paper_end.get('m2'), 'папка ручная')
    shtamp_res = resp(a, b, c)

    currency = {'euro': currency_req, 'rub': 1}
    data_calc = calc_count.objects.get(style_work=type_work)
    cardboard_obj = Material.objects.get(mt_name=cardboard_req)
    paper_obj = Material.objects.get(mt_name=paper_req)

    paper_count = (paper_obj.prise * (currency.get(paper_obj.currency))*result_paper)
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
            'Расход бумаги': result_paper,
            'Работа': float(toFixed(work, 2)),
            'Цены': calc_sum,
            'Цена штампа': float(toFixed(shtamp_res, 2))}
    return data