from cubbox.calculate import Cardboard_Box, Paper_Box_Hand, Paper_Box_Auto
from cub_box_0.models import Work, Material, calc_count, Work2
from cubbox.shtamp import cutter
from details.algprog.toFix import toFixed
from services.marga import marga, prices


def machin_work(res_paper, kol):
    object_list = Work.objects.all()
    for obj in object_list:
        if obj.Name == 'крышка_авто' and obj.dm2 <= res_paper[0]:
            lid = ((obj.Content + obj.Scotch) + (obj.Close_fitting / kol)) + obj.Lid
        elif obj.Name == 'дно_авто' and obj.dm2 <= res_paper[1]:
            tray = ((obj.Content + obj.Scotch) + (obj.Close_fitting / kol)) + obj.Tray
    return [lid, tray]


def hand_work(a, b, hight):
    object_list = Work2.objects.all()
    size_box = a+b
    work_count = None
    for obj in object_list:
        if size_box <= obj.Size and hight <= obj.Hight:
            work_count = obj.Count
            break
    return work_count


def result_data_box(a, b, c, cardboard_req, paper_req, kol, lid_hight, currency_req):
    # толщина картона
    thickness_cb = Material.objects.get(mt_name=cardboard_req).len
    # размер листа материала
    lissiz_cb = [Material.objects.get(mt_name=cardboard_req).size_x, Material.objects.get(mt_name=cardboard_req).size_y]
    lissiz_pap = [Material.objects.get(mt_name=paper_req).size_x, Material.objects.get(mt_name=paper_req).size_y]

    if kol >= 500 and a >= 80 and b >= 65 and c >= 10:
        # расчет изготовления на автоматической машине
        if a <= 460 and b <= 380 and c <= 120:
            cardboard = Cardboard_Box(a, b, c, thickness_cb, lid_hight).cardboard_box(lis_siz=lissiz_cb)
            paper = Paper_Box_Auto(a, b, c, thickness_cb, lid_hight).cub_box_paper(lis_siz=lissiz_pap)
            # расход материала
            result_cardboard = cardboard['Расход']
            result_paper = paper['Расход']
            # информация
            info_cardboard_paper = {'Картон': cardboard.get("Информация"),
                                    'Бумага': paper.get("Информация")}

            lid = machin_work(paper['m2'], kol)[0]
            tray = machin_work(paper['m2'], kol)[1]
            # стоимость работы
            work = lid+tray
            type_work = ['Сборка автоматическая.', 'кд автомат']
            # стоимость штампа
            shtamp_res = cutter(a, b, c, lid_hight)*2

        # расчет изготовления лотка вручную
        else:
            cardboard = Cardboard_Box(a, b, c, thickness_cb, lid_hight).cardboard_box(lis_siz=lissiz_cb)
            paper = Paper_Box_Hand(a, b, c, thickness_cb, lid_hight).cub_box_paper(lis_siz=lissiz_pap)
            # расход материала
            result_cardboard = cardboard['Расход']
            result_paper = paper['Расход']
            # информация
            info_cardboard_paper = {'Картон': cardboard.get("Информация"),
                                    'Бумага': paper.get("Информация")}
            # стоимость работы
            work = hand_work(a, b, c)
            type_work = ['Сборка ручная.', 'кд ручное']
            # стоимость штампа
            shtamp_res = cutter(a, b, c, lid_hight)

    # расчет изготовления лотка вручную
    else:
        cardboard = Cardboard_Box(a, b, c, thickness_cb, lid_hight).cardboard_box(lis_siz=lissiz_cb)
        paper = Paper_Box_Hand(a, b, c, thickness_cb, lid_hight).cub_box_paper(lis_siz=lissiz_pap)
        # расход материала
        result_cardboard = cardboard['Расход']
        result_paper = paper['Расход']
        # информация
        info_cardboard_paper = {'Картон': cardboard.get("Информация"),
                                'Бумага': paper.get("Информация")}
        # стоимость работы
        work = hand_work(a, b, c)
        type_work = ['Сборка ручная.', 'кд ручное']
        # стоимость штампа
        shtamp_res = cutter(a, b, c, lid_hight)

    currency = {'euro': currency_req, 'rub': 1}
    # расчетные данные для калькуляции стоимости
    data_calc = calc_count.objects.get(style_work=type_work[1])
    # материал
    cardboard_obj = Material.objects.get(mt_name=cardboard_req)
    paper_obj = Material.objects.get(mt_name= paper_req)
    # стоимость бумаги перемноженная на расход бумаги
    paper_count = (paper_obj.prise * (currency.get(paper_obj.currency))*result_paper)
    # стоимость картона перемноженная на расход картона
    cardboard_count = (cardboard_obj.prise * (currency.get(cardboard_obj.currency))*result_cardboard)
    # подсчет всех производственных затрат
    production_cost = (paper_count+cardboard_count)*data_calc.reject+data_calc.cut+(work)+((work)\
                                                                        *data_calc.not_production)
    # стоимости
    calc_sum = marga(production_cost)

    data = {'Информация о коробке': f'Размер коробки {a}x{b}x{c}мм. Высота крышки {lid_hight}. Тираж {kol}шт. '
                                    f'Картон - {cardboard_req}. Бумага - {paper_req}. ',
            'Расходы': f'Расход картона - {toFixed(result_cardboard, 2)}л. Расход бумаги - {toFixed(result_paper, 2)}л. ',
            'Информация картон': info_cardboard_paper['Картон'],
            'Информация бумага': info_cardboard_paper['Бумага'],
            'Работа': f'Стоимость работы - {work} руб. {type_work[0]}',
            'Цены': prices(calc_sum),
            'Цена штампа': f'Цена штампа - {toFixed(shtamp_res, 2)} руб.'}
    print(data)
    return data
