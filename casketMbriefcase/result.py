from casketMbriefcase.caskethand.result import result_data_casket_hand
from casketMbriefcase.casketauto.result import result_data_casket_auto
from details.algprog.toFix import toFixed
from services.marga import prices


def result_data_briefcase(a, b, c, cardboard_req, paper_req, kol, cur_euro, handle):
    if kol >= 500 and a >= 80 and b >= 65 and c >= 10:
        # расчет изготовления лотка на автоматической машине
        if a <= 460 and b <= 380 and c <= 120:
            result = result_data_casket_auto(a, b, c, cardboard_req, paper_req, cur_euro, handle)
            # расход материала
            result_cardboard = result.get('Расход картона')
            result_paper = result.get('Расход бумаги')
            # стоимость работы
            type_work_tray = 'Сборка автоматическая лотка.'
            work = f'папка {result["Работа"]["папка"]}руб, лоток {result["Работа"]["лоток"]}руб'
            # стоимость штампа
            shtamp_res = result.get('Цена штампа')
            # склейка стоимости
            calc_sum = result.get('Цены')

        # расчет изготовления лотка вручную
        else:
            result = result_data_casket_hand(a, b, c, cardboard_req, paper_req, cur_euro, handle)
            # расход материала
            result_cardboard = result.get('Расход картона')
            result_paper = result.get('Расход бумаги')
            # стоимость работы
            type_work_tray = 'Сборка ручная лотка.'
            work = f'папка {result["Работа"]["папка"]}руб, лоток {result["Работа"]["лоток"]}руб'
            # стоимость штампа
            shtamp_res = result.get('Цена штампа')
            # склейка стоимости
            calc_sum = result.get('Цены')

    # расчет изготовления лотка вручную
    else:
        result = result_data_casket_hand(a, b, c, cardboard_req, paper_req, cur_euro, handle)
        # расход материала
        result_cardboard = result.get('Расход картона')
        result_paper = result.get('Расход бумаги')
        # стоимость работы
        type_work_tray = 'Сборка ручная лотка.'
        work = f'папка {result["Работа"]["папка"]}руб, лоток {result["Работа"]["лоток"]}руб'
        # стоимость штампа
        shtamp_res = result.get('Цена штампа')
        # склейка стоимости
        calc_sum = result.get('Цены')

    data = {'Информация о коробке': f'Размер коробки {a}x{b}x{c}мм. Тираж {kol}шт. '
                                    f'Ручка - {handle}. '
                                    f'Картон - {cardboard_req}. Бумага - {paper_req}. ',
            'Расходы': f'Расход картона - {toFixed(result_cardboard, 2)}л. Расход бумаги - {toFixed(result_paper, 2)}л. ',
            'Информация картон': result.get('Информация')['Картон'],
            'Информация бумага': result.get('Информация')['Бумага'],
            'Работа': f'Стоимость работы - {work}. {type_work_tray}',
            'Цены': prices(calc_sum),
            'Цена штампа': f'Цена штампа - {toFixed(shtamp_res, 2)} руб.'}
    print(data)
    return data

