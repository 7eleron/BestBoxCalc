from details.tray.trayauto.result import result_data_tray_auto
from details.tray.trayhandcasket.result import result_data_tray_hand
from details.folder.folderM.folderhand.result import result_data_folder_hand
from details.algprog.toFix import toFixed
from services.marga import glue_price, prices


def result_data_casket(a, b, c, cardboard_req, paper_req, kol, cur_euro):
    if kol >= 500 and a >= 80 and b >= 65 and c >= 10:
        # расчет изготовления лотка на автоматической машине
        if a <= 460 and b <= 380 and c <= 120:
            tray = result_data_tray_auto(a, b, c, cardboard_req, paper_req, cur_euro)
            folder = result_data_folder_hand(a, b, c, cardboard_req, paper_req, cur_euro)
            # расход материала
            result_cardboard = tray.get('Расход картона')+folder.get('Расход картона')
            result_paper = tray.get('Расход бумаги')+folder.get('Расход бумаги')
            # стоимость работы
            type_work_tray = 'Сборка автоматическая лотка. '
            work = f'папка {folder.get("Работа")}руб, лоток {tray.get("Работа")}руб'
            # стоимость штампа
            shtamp_res = tray.get('Цена штампа')+folder.get('Цена штампа')
            # склейка стоимости
            calc_sum = glue_price(tray.get('Цена'), folder.get('Цены'))

        # расчет изготовления лотка вручную
        else:
            tray = result_data_tray_hand(a, b, c, cardboard_req, paper_req, cur_euro)
            folder = result_data_folder_hand(a, b, c, cardboard_req, paper_req, cur_euro)
            # расход материала
            result_cardboard = tray.get('Расход картона') + folder.get('Расход картона')
            result_paper = tray.get('Расход бумаги') + folder.get('Расход бумаги')
            # стоимость работы
            type_work_tray = 'Сборка ручная лотка.'
            work = f'папка {folder.get("Работа")}руб, лоток {tray.get("Работа")}руб'
            # стоимость штампа
            shtamp_res = tray.get('Цена штампа') + folder.get('Цена штампа')
            # склейка стоимости
            calc_sum = glue_price(tray.get('Цена'), folder.get('Цены'))

    # расчет изготовления лотка вручную
    else:
        tray = result_data_tray_hand(a, b, c, cardboard_req, paper_req, cur_euro)
        folder = result_data_folder_hand(a, b, c, cardboard_req, paper_req, cur_euro)
        # расход материала
        result_cardboard = tray.get('Расход картона') + folder.get('Расход картона')
        result_paper = tray.get('Расход бумаги') + folder.get('Расход бумаги')
        # стоимость работы
        type_work_tray = 'Сборка ручная лотка.'
        work = f'папка {folder.get("Работа")}руб, лоток {tray.get("Работа")}руб'
        # стоимость штампа
        shtamp_res = tray.get('Цена штампа') + folder.get('Цена штампа')
        # склейка стоимости
        calc_sum = glue_price(tray.get('Цены'), folder.get('Цены'))

    data = {'Информация о коробке': f'Размер коробки {a}x{b}x{c}мм. Тираж {kol}шт. '
                                    f'Картон - {cardboard_req}. Бумага - {paper_req}. ',
            'Расходы': f'Расход картона - {toFixed(result_cardboard, 2)}л. Расход бумаги - {toFixed(result_paper, 2)}л. ',
            'Информация крышка': folder.get('Информация'),
            'Информация дно': tray.get('Информация'),
            'Работа': f'Стоимость работы - {work}. {type_work_tray}',
            'Цены': prices(calc_sum),
            'Цена штампа': f'Цена штампа - {toFixed(shtamp_res, 2)} руб.'}
    print(data)
    return data

