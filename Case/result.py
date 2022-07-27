from details.tray.trayauto.result import result_data_tray_auto
from details.tray.trayhand.result import result_data_tray_hand
from details.case.casehand.result import result_data_case_hand
from details.algprog.toFix import toFixed


def result_data_case(a, b, c, cardboard_req, paper_req, kol, cur_euro):
    calc_sum = []
    if kol >= 500 and a >= 80 and b >= 65 and c >= 10:
        if a <= 460 and b <= 380 and c <= 120:
            type_work_tray = 'Сборка автоматическая лотка. '
            tray = result_data_tray_auto(a, b, c, cardboard_req, paper_req, cur_euro)
            case = result_data_case_hand(a, b, c, cardboard_req, paper_req, cur_euro)
            result_cardboard = tray.get('Расход картона')+case.get('Расход картона')
            result_paper = tray.get('Расход бумаги')+case.get('Расход бумаги')
            work = f'папка {case.get("Работа")}руб, лоток {tray.get("Работа")}руб'
            shtamp_res = tray.get('Цена штампа')+case.get('Цена штампа')
            for x in range(7):
                calc_sum.append(toFixed(tray.get('Цена')[x] + case.get('Цены')[x], 2))
        else:
            type_work_tray = 'Сборка ручная лотка.'
            tray = result_data_tray_hand(a, b, c, cardboard_req, paper_req, cur_euro)
            case = result_data_case_hand(a, b, c, cardboard_req, paper_req, cur_euro)
            result_cardboard = tray.get('Расход картона') + case.get('Расход картона')
            result_paper = tray.get('Расход бумаги') + case.get('Расход бумаги')
            work = f'футляр {case.get("Работа")}руб, лоток {tray.get("Работа")}руб'
            shtamp_res = tray.get('Цена штампа') + case.get('Цена штампа')
            for x in range(7):
                calc_sum.append(toFixed(tray.get('Цена')[x] + case.get('Цены')[x], 2))
    else:
        type_work_tray = 'Сборка ручная лотка.'
        tray = result_data_tray_hand(a, b, c, cardboard_req, paper_req, cur_euro)
        case = result_data_case_hand(a, b, c, cardboard_req, paper_req, cur_euro)
        result_cardboard = tray.get('Расход картона') + case.get('Расход картона')
        result_paper = tray.get('Расход бумаги') + case.get('Расход бумаги')
        work = f'футляр {case.get("Работа")}руб, лоток {tray.get("Работа")}руб'
        shtamp_res = tray.get('Цена штампа') + case.get('Цена штампа')
        for x in range(7):
            calc_sum.append(toFixed(tray.get('Цены')[x] + case.get('Цены')[x], 2))

    data = {'Информация о коробке': f'Размер коробки {a}x{b}x{c}мм. Тираж {kol}шт. '
                                    f'Картон - {cardboard_req}. Бумага - {paper_req}. ',
            'Расходы': f'Расход картона - {toFixed(result_cardboard, 2)}л. Расход бумаги - {toFixed(result_paper, 2)}л. ',
            'Работа': f'Стоимость работы - {work}. {type_work_tray}',
            'Цены': f'Цена коробки: 40% - {calc_sum[0]} руб/шт. '
                    f'50% - {calc_sum[1]} руб/шт. '
                    f'60% - {calc_sum[2]} руб/шт. '
                    f'70% - {calc_sum[3]} руб/шт. '
                    f'80% - {calc_sum[4]} руб/шт. '
                    f'90% - {calc_sum[5]} руб/шт. '
                    f'100% - {calc_sum[6]} руб/шт. ',
            'Цена штампа': f'Цена штампа - {toFixed(shtamp_res, 2)} руб.'}
    print(data)
    return data

