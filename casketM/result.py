from details.tray.trayauto.result import result_data_tray_auto
from details.tray.trayhandcasket.result import result_data_tray_hand
from details.folder.folderM.folderhand.result import result_data_folder_hand
from details.algprog.toFix import toFixed


def result_data_casket(a, b, c, cardboard_req, paper_req, kol):
    calc_sum = []
    if kol >= 500 and a >= 80 and b >= 65 and c >= 10:
        if a <= 460 and b <= 380 and c <= 120:
            type_work_tray = 'Сборка автоматическая лотка. '
            tray = result_data_tray_auto(a, b, c, cardboard_req, paper_req)
            folder = result_data_folder_hand(a, b, c, cardboard_req, paper_req)
            result_cardboard = tray.get('Расход картона')+folder.get('Расход картона')
            result_paper = tray.get('Расход бумаги')+folder.get('Расход бумаги')
            work = f'папка {folder.get("Работа")}руб, лоток {tray.get("Работа")}руб'
            shtamp_res = tray.get('Цена штампа')+folder.get('Цена штампа')
            for x in range(7):
                calc_sum.append(toFixed(tray.get('Цена')[x] + folder.get('Цены')[x], 2))
        else:
            type_work_tray = 'Сборка ручная лотка.'
            tray = result_data_tray_hand(a, b, c, cardboard_req, paper_req)
            folder = result_data_folder_hand(a, b, c, cardboard_req, paper_req)
            result_cardboard = tray.get('Расход картона') + folder.get('Расход картона')
            result_paper = tray.get('Расход бумаги') + folder.get('Расход бумаги')
            work = f'папка {folder.get("Работа")}руб, лоток {tray.get("Работа")}руб'
            shtamp_res = tray.get('Цена штампа') + folder.get('Цена штампа')
            for x in range(7):
                calc_sum.append(toFixed(tray.get('Цена')[x] + folder.get('Цены')[x], 2))
    else:
        type_work_tray = 'Сборка ручная лотка.'
        tray = result_data_tray_hand(a, b, c, cardboard_req, paper_req)
        folder = result_data_folder_hand(a, b, c, cardboard_req, paper_req)
        result_cardboard = tray.get('Расход картона') + folder.get('Расход картона')
        result_paper = tray.get('Расход бумаги') + folder.get('Расход бумаги')
        work = f'папка {folder.get("Работа")}руб, лоток {tray.get("Работа")}руб'
        shtamp_res = tray.get('Цена штампа') + folder.get('Цена штампа')
        for x in range(7):
            calc_sum.append(toFixed(tray.get('Цены')[x] + folder.get('Цены')[x], 2))
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
            'Цена штампа': f'Цена штампа - {shtamp_res} руб.'}
    return data

