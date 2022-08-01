from details.cubboxinsert.cbinserthand.calculate import ExpenceCubBoxInsert
from cub_box_0.models import Material, calc_count
from details.cubboxinsert.cbinsertauto.shtamp import resp
from details.algprog.toFix import toFixed
from services.marga import marga
from work.hand_work_cubbox import hand_work


def result_data_cdinsert_hand(a, b, tray_hight, lid_hight, insert_hight, cardboard_req, paper_req, currency_req):
    # толщина картона
    thickness_cb = Material.objects.get(mt_name=cardboard_req).len
    # размер листа материала
    lissiz_cb = [Material.objects.get(mt_name=cardboard_req).size_x, Material.objects.get(mt_name=cardboard_req).size_y]
    lissiz_pap = [Material.objects.get(mt_name=paper_req).size_x, Material.objects.get(mt_name=paper_req).size_y]

    # расход материала
    obj_cbinsert = ExpenceCubBoxInsert(a, b, tray_hight, lid_hight, insert_hight, thickness_cb)
    cardboard = obj_cbinsert.result(lissiz_cb)['cardboard']
    paper = obj_cbinsert.result(lissiz_pap)['paper']
    # расход материала
    result_cardboard = cardboard.get('Расход')
    result_paper = paper.get('Расход')
    # информация
    info_cardboard_paper = f'Картон - {cardboard.get("Информация")} ' \
                           f'Бумага - {paper.get("Информация")} '
    # стоимость работы
    type_work = 'кд автомат'
    work = hand_work(a, b, tray_hight+lid_hight)*1.2
    # стоимость штампа
    shtamp_res = resp(a, b, tray_hight, lid_hight, insert_hight)

    currency = {'euro': currency_req, 'rub': 1}
    # расчетные данные для калькуляции стоимости
    data_calc = calc_count.objects.get(style_work=type_work)
    # материал
    paper_obj = Material.objects.get(mt_name=paper_req)
    cardboard_obj = Material.objects.get(mt_name=cardboard_req)
    # стоимость бумаги перемноженная на расход бумаги
    paper_count = (paper_obj.prise * (currency.get(paper_obj.currency))*result_paper)
    # стоимость картона перемноженная на расход картона
    cardboard_count = (cardboard_obj.prise * (currency.get(cardboard_obj.currency))*result_cardboard)
    # подсчет всех производственных затрат
    production_cost = (paper_count+cardboard_count)*data_calc.reject+data_calc.cut+work+((work)\
                                                                        *data_calc.not_production)
    # стоимости
    calc_sum = marga(production_cost)

    data = {'Расход картона': result_cardboard,
            'Расход бумаги': result_paper,
            'Информация': info_cardboard_paper,
            'Работа': float(toFixed(work, 2)),
            'Цены': calc_sum,
            'Цена штампа': toFixed(shtamp_res, 2)}
    return data
