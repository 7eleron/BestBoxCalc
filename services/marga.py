from details.algprog.toFix import toFixed


# цены
def prices(calc_sum: list):
    return f'Цена коробки: 30% - {calc_sum[0]} руб/шт. '\
                         f'40% - {calc_sum[1]} руб/шт. '\
                         f'50% - {calc_sum[2]} руб/шт. '\
                         f'60% - {calc_sum[3]} руб/шт. '\
                         f'70% - {calc_sum[4]} руб/шт. '\
                         f'80% - {calc_sum[5]} руб/шт. '\
                         f'90% - {calc_sum[6]} руб/шт. '\
                         f'100% - {calc_sum[7]} руб/шт. '


# маржа
def marga(production_cost):
    listsum = [((production_cost * 0.3) * 1.1) + production_cost,
               ((production_cost * 0.4) * 1.1) + production_cost,
               ((production_cost * 0.5) * 1.1) + production_cost,
               ((production_cost * 0.6) * 1.1) + production_cost,
               ((production_cost * 0.7) * 1.1) + production_cost,
               ((production_cost * 0.8) * 1.1) + production_cost,
               ((production_cost * 0.9) * 1.1) + production_cost,
               ((production_cost * 1) * 1.1) + production_cost
               ]
    listsum = [float(toFixed(x, 2)) for x in listsum]
    return listsum


# склейка двух цен
def glue_price(first: list, second: list):
    calc_sum = []
    for x in range(8):
        calc_sum.append(toFixed(first[x] + second[x], 2))
    return calc_sum
