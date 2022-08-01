from details.folder.folderM.folderhand.calculate import ExpenceFolder
from cub_box_0.models import Material, calc_count
from details.folder.folderM.folderhand.shtamp import resp
from details.algprog.toFix import toFixed
from services.marga import marga
from work.hand_work_folder import folder_work


def result_data_folder_hand(a, b, c, cardboard_req, paper_req, cur_euro):
    currency_req = cur_euro
    # толщина картона
    thickness_cb = Material.objects.get(mt_name=cardboard_req).len
    # размер листа материала
    lissiz_cb = [Material.objects.get(mt_name=cardboard_req).size_x, Material.objects.get(mt_name=cardboard_req).size_y]
    lissiz_pap = [Material.objects.get(mt_name=paper_req).size_x, Material.objects.get(mt_name=paper_req).size_y]

    type_work = 'папка магниты ручная'
    obj_folder = ExpenceFolder(a, b, c, thickness_cb)
    cardboard = obj_folder.result(lissiz_cb)['cardboard']
    paper_fold = obj_folder.result(lissiz_pap).get('paper_folder')
    paper_end = obj_folder.result(lissiz_pap).get('paper_end')
    # расход материала
    result_cardboard = cardboard.get('Расход')
    result_paper = paper_fold.get('Расход')+paper_end.get('Расход')
    # информация
    info_cardboard_paper = f'Картон - {cardboard.get("Информация")}. ' \
                           f'Бумага - {paper_fold.get("Информация")}{paper_end.get("Информация")}. '

    m2 = paper_fold.get('m2')+paper_end.get('m2')
    # стоимость работы
    work = folder_work(m2)*m2
    # стоимость штампа
    shtamp_res = resp(a, b, c)

    currency = {'euro': currency_req, 'rub': 1}
    # расчетные данные для калькуляции стоимости
    data_calc = calc_count.objects.get(style_work=type_work)
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

    # подсчет всех производственных затрат
    production_cost = ((paper_count+cardboard_count)*data_calc.reject)+magnets+data_calc.cut+work+((work)\
                                                                        *data_calc.not_production)
    # стоимости
    calc_sum = marga(production_cost)

    data = {'Расход картона': result_cardboard,
            'Расход бумаги': result_paper,
            'Информация': info_cardboard_paper,
            'Работа': float(toFixed(work, 2)),
            'Цены': calc_sum,
            'Цена штампа': float(toFixed(shtamp_res, 2))}
    return data
