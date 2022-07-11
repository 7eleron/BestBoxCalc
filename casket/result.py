from casket.calculate import Cardboard_Casket, Paper_Casket
from cub_box_0.models import Work, Material, calc_count, Work2
from alg_prog.currency import currency_eur as cur_euro
from casket.shtamp import resp
from alg_prog.toFix import toFixed


def machin_work(res_paper):
    object_list = Work.objects.all()
    for obj in object_list:
        if obj.Name == 'дно_авто' and obj.dm2 <= res_paper[1]:
            tray = obj.Tray
    return tray


def hand_work_tray(a, b, hight):
    object_list = Work2.objects.all()
    size_box = a+b
    work_count = None
    for obj in object_list:
        if size_box <= obj.Size and hight <= obj.Hight:
            work_count = obj.Count
            break
    return work_count/2.5


def folder_work(list, type_work):
    m2 = list[0]+list[2]
    object = Work.objects.get(Name=type_work).Lid
    return object * m2


def result_data_casket(a, b, c, cardboard_req, paper_req, kol):
    currency_req = cur_euro()
    thickness_cb = Material.objects.get(mt_name=cardboard_req).len
    lis_siz = [Material.objects.get(mt_name=cardboard_req).size_x, Material.objects.get(mt_name=cardboard_req).size_y]

    if kol >= 500 and a >= 80 and b >= 65 and c >= 10:
        if a <= 460 and b <= 380 and c <= 120:
            type_work = ['Сборка автоматическая лотка. ', 'шкатулка автомат']
            cardboard = Cardboard_Casket(a, b, c, thickness_cb)
            result_cardboard = cardboard.cardboard_casket(lis_siz)
            paper = Paper_Casket(a, b, c, thickness_cb)
            result_paper = paper.paper_casket(lis_siz, type_work[1])
            work_fold = folder_work(result_paper.get('m2'), 'папка автомат')
            work_tray = machin_work(result_paper.get('m2'))
            object_scotch = Work.objects.get(Name='папка автомат').Scotch
            work = work_tray + work_fold + object_scotch
            shtamp_res = resp(a, b, c)

        else:
            type_work = ['Сборка ручная. ', 'шкатулка ручная']
            cardboard = Cardboard_Casket(a, b, c, thickness_cb)
            result_cardboard = cardboard.cardboard_casket(lis_siz)
            paper = Paper_Casket(a, b, c, thickness_cb)
            result_paper = paper.paper_casket(lis_siz, type_work[1])
            work_tray = hand_work_tray(a, b, c)
            work_fold = folder_work(result_paper.get('m2'), 'папка ручная')
            object_scotch = Work.objects.get(Name='папка ручная').Scotch
            work = work_tray + work_fold + object_scotch
            shtamp_res = resp(a, b, c)
    else:
        type_work = ['Сборка ручная. ', 'шкатулка ручная']
        cardboard = Cardboard_Casket(a, b, c, thickness_cb)
        result_cardboard = cardboard.cardboard_casket(lis_siz)
        paper = Paper_Casket(a, b, c, thickness_cb)
        result_paper = paper.paper_casket(lis_siz, type_work[1])
        work_tray = hand_work_tray(a, b, c)
        work_fold = folder_work(result_paper.get('m2'), 'папка ручная')
        object_scotch = Work.objects.get(Name='папка ручная').Scotch
        work = work_tray + work_fold + object_scotch
        shtamp_res = resp(a, b, c)

    currency = {'euro': currency_req, 'rub': 1}
    data_calc = calc_count.objects.get(style_work=type_work[1])
    paper_obj = Material.objects.get(mt_name= paper_req)
    paper_count = (paper_obj.prise * (currency.get(paper_obj.currency))*float(result_paper.get('except')))
    cardboard_obj = Material.objects.get(mt_name= cardboard_req)
    cardboard_count = (cardboard_obj.prise * (currency.get(cardboard_obj.currency))*float(result_cardboard))
    production_cost = (paper_count+cardboard_count)*data_calc.reject+data_calc.cut+(work)+((work)\
                                                                        *data_calc.not_production)
    calc_sum = ((production_cost*data_calc.margin)*data_calc.manager_proc)+production_cost

    data = f'Размер коробки {a}x{b}x{c}мм. Тираж {kol}шт.' \
           f'\nРасход картона - {toFixed(result_cardboard, 2)}л. ' \
           f'\nРасход бумаги - {result_paper.get("except")}л. {result_paper.get("info")}' \
           f'\nСтоимость работы - папка: {toFixed(work_fold, 2)}руб; лоток: {toFixed(work_tray, 2)}руб; ' \
           f'сборка: {object_scotch}руб. {type_work[0]} ' \
           f'\nКартон - {cardboard_req}. Бумага - {paper_req}.' \
           f'\nЦена коробки - {toFixed(calc_sum, 2)} руб/шт.' \
           f'\nЦена штампа - {toFixed(shtamp_res, 2)} руб.'
    return data

