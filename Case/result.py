from details.tray.trayauto.result import result_data_tray_auto
from details.tray.trayhand.result import result_data_tray_hand
from details.case.casehand.result import result_data_case_hand
from details.algprog.toFix import toFixed
from services.marga import prices, glue_price


def result_data_case(a, b, c, cardboard_req, paper_req, kol, cur_euro):

    if kol >= 500 and a >= 80 and b >= 65 and c >= 10:
        # расчет изготовления лотка на автоматической машине
        if a <= 460 and b <= 380 and c <= 120:
            tray = result_data_tray_auto(a, b, c, cardboard_req, paper_req, cur_euro)
            case = result_data_case_hand(a, b, c, cardboard_req, paper_req, cur_euro)
            # расход материала
            result_cardboard = tray.get('Расход картона')+case.get('Расход картона')
            result_paper = tray.get('Расход бумаги')+case.get('Расход бумаги')
            # стоимость работы
            type_work_tray = 'Сборка автоматическая лотка. '
            work = f'папка {case.get("Работа")}руб, лоток {tray.get("Работа")}руб'
            # стоимость штампа
            shtamp_res = tray.get('Цена штампа')+case.get('Цена штампа')
            # склейка стоимости
            calc_sum = glue_price(tray.get('Цены'), case.get('Цены'))

        # расчет изготовления лотка вручную
        else:
            tray = result_data_tray_hand(a, b, c, cardboard_req, paper_req, cur_euro)
            case = result_data_case_hand(a, b, c, cardboard_req, paper_req, cur_euro)
            # расход материала
            result_cardboard = tray.get('Расход картона') + case.get('Расход картона')
            result_paper = tray.get('Расход бумаги') + case.get('Расход бумаги')
            # стоимость работы
            type_work_tray = 'Сборка ручная лотка.'
            work = f'футляр {case.get("Работа")}руб, лоток {tray.get("Работа")}руб'
            # стоимость штампа
            shtamp_res = tray.get('Цена штампа') + case.get('Цена штампа')
            # склейка стоимости
            calc_sum = glue_price(tray.get('Цены'), case.get('Цены'))

    # расчет изготовления лотка вручную
    else:
        tray = result_data_tray_hand(a, b, c, cardboard_req, paper_req, cur_euro)
        case = result_data_case_hand(a, b, c, cardboard_req, paper_req, cur_euro)
        # расход материала
        result_cardboard = tray.get('Расход картона') + case.get('Расход картона')
        result_paper = tray.get('Расход бумаги') + case.get('Расход бумаги')
        # стоимость работы
        type_work_tray = 'Сборка ручная лотка.'
        work = f'футляр {case.get("Работа")}руб, лоток {tray.get("Работа")}руб'
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
    print(data)
    return data

