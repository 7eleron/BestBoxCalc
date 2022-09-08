from CubBoxInsert.cubboxinsert.cbinsertauto.result import result_data_cdinsert_auto
from CubBoxInsert.cubboxinsert.cbinserthand.result import result_data_cdinsert_hand
from details.algprog.toFix import toFixed
from services.marga import prices


def result_data_cdinsert(a, b, tray_hight, insert_hight, cardboard_req, paper_req, kol, lid_hight, cur_euro, lam_req):
    if kol >= 500 and a >= 80 and b >= 65 and tray_hight >= 10 and lid_hight >= 10 and insert_hight >= 10:
        # расчет изготовления лотка на автоматической машине
        if a <= 460 and b <= 380 and tray_hight <= 120 and lid_hight <= 120 and insert_hight <= 120:
            result = result_data_cdinsert_auto(a, b, tray_hight, lid_hight, insert_hight, cardboard_req, paper_req,
                                               cur_euro, kol, laminating=lam_req)
            # расход материала
            result_cardboard = result.get('Расход картона')
            result_paper = result.get('Расход бумаги')
            # стоимость работы
            type_work_tray = 'Сборка автоматическая. '
            work = f'{result.get("Работа")}руб '
            # стоимость штампа
            shtamp_res = result.get('Цена штампа')
            # склейка стоимости
            calc_sum = result.get('Цены')

        # расчет изготовления лотка вручную
        else:
            result = result_data_cdinsert_hand(a, b, tray_hight, lid_hight, insert_hight, cardboard_req, paper_req,
                                               cur_euro, kol, laminating=lam_req)
            # расход материала
            result_cardboard = result.get('Расход картона')
            result_paper = result.get('Расход бумаги')
            # стоимость работы
            type_work_tray = 'Сборка ручная. '
            work = f'{result.get("Работа")}руб '
            # стоимость штампа
            shtamp_res = result.get('Цена штампа')
            # склейка стоимости
            calc_sum = result.get('Цены')

    # расчет изготовления лотка вручную
    else:
        result = result_data_cdinsert_hand(a, b, tray_hight, lid_hight, insert_hight, cardboard_req, paper_req,
                                           cur_euro, kol, laminating=lam_req)
        # расход материала
        result_cardboard = result.get('Расход картона')
        result_paper = result.get('Расход бумаги')
        # стоимость работы
        type_work_tray = 'Сборка ручная. '
        work = f'{result.get("Работа")}руб '
        # стоимость штампа
        shtamp_res = result.get('Цена штампа')
        # склейка стоимости
        calc_sum = result.get('Цены')

    if tray_hight+lid_hight >= insert_hight:
        all_hight = tray_hight+lid_hight
    else:
        all_hight = insert_hight

    data = {'Информация о коробке': f'Размер коробки {a}x{b}x{all_hight}мм. '
                                    f'Крышка {lid_hight}мм, дно {tray_hight}мм, вставка {insert_hight}мм. Тираж {kol}шт. '
                                    f'Картон - {cardboard_req}. Бумага - {paper_req}. ',
            'Расходы': f'Расход картона - {toFixed(result_cardboard, 2)}л. Расход бумаги - {toFixed(result_paper, 2)}л. ',
            'Информация картон': result.get('Информация')['Картон'],
            'Информация бумага': result.get('Информация')['Бумага'],
            'Работа': f'Стоимость работы - {work}. {type_work_tray}',
            'Цены': prices(calc_sum),
            'Цена штампа': f'Цена штампа - {shtamp_res} руб.'}
    print(data)
    return data

