from details.algprog.currency import currency_eur


def responseresult(result):
    return {'cur_euro': currency_eur(),
            'info': result.get('Информация о коробке'),
            'expence': result.get('Расходы'),
            'work': result.get('Работа'),
            'prices': result.get('Цены'),
            'priceshtamp': result.get('Цена штампа'),
            'infocb': result.get('Информация картон'),
            'infotpap': result.get('Информация бумага'),
            }
