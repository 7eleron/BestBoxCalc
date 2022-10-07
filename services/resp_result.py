from details.algprog.currency import currency_eur


def responseresult(result):
    return {'cur_euro': currency_eur(),
            'info': result.get('Информация о коробке'),
            'material': result.get('Материал'),
            'expence': result.get('Расходы'),
            'work': result.get('Работа'),
            'prices': result.get('Цены'),
            'priceshtamp': result.get('Цена штампа'),
            'count_all': result.get('Цена заказа'),
            'sebek': result.get('Себек'),
            'marga': result.get('Маржа'),
            'procmanager': result.get('Процент менеджера'),
            'infocb': result.get('Информация картон'),
            'infotpap': result.get('Информация бумага'),
            }
