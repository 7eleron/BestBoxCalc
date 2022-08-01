

def calculate_data(a, b, tray_hight, lid_hight, insert_hight, cardboard_req, paper_req, kol, cur_euro):
    tray = result_data_cdinsert_auto(a, b, tray_hight, lid_hight, insert_hight, cardboard_req, paper_req, cur_euro)
    case = result_data_case_hand(a, b, c, cardboard_req, paper_req, cur_euro)
    # расход материала
    result_cardboard = tray.get('Расход картона') + case.get('Расход картона')
    result_paper = tray.get('Расход бумаги') + case.get('Расход бумаги')
    # стоимость работы
    type_work_tray = 'Сборка автоматическая лотка. '
    work = f'папка {case.get("Работа")}руб, лоток {tray.get("Работа")}руб'
    # стоимость штампа
    shtamp_res = tray.get('Цена штампа') + case.get('Цена штампа')
    # склейка стоимости
    calc_sum = glue_price(tray.get('Цены'), case.get('Цены'))

    data = {'Информация о коробке': f'Размер коробки {a}x{b}x{c}мм. Тираж {kol}шт. '
                                    f'Картон - {cardboard_req}. Бумага - {paper_req}. ',
            'Расходы': f'Расход картона - {toFixed(result_cardboard, 2)}л. Расход бумаги - {toFixed(result_paper, 2)}л. ',
            'Информация крышка': case.get('Информация'),
            'Информация дно': tray.get('Информация'),
            'Работа': f'Стоимость работы - {work}. {type_work_tray}',
            'Цены': prices(calc_sum),
            'Цена штампа': f'Цена штампа - {toFixed(shtamp_res, 2)} руб.'}

    return data
