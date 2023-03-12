"""def calc(lis, lis_siz):
    kol_lis = 0
    var = None
    for x in lis:
        print('--- 1 ---')
        # проход по длинной стороне
        ras_0 = (lis_siz[0]//x[0])*(lis_siz[1]//x[1])
        ras_ost_0 = [[lis_siz[0] % x[0], lis_siz[1]], [lis_siz[1] % x[1], lis_siz[0]]]
        kol_ost_ras_0_1 = (ras_ost_0[0][0] // x[1]) * (ras_ost_0[0][1] // x[0])
        kol_ost_ras_0_2 = (ras_ost_0[0][0] // x[0]) * (ras_ost_0[0][1] // x[1])

        if kol_ost_ras_0_1 > kol_ost_ras_0_2:
            kol_dop_ras_0 = kol_ost_ras_0_1
        else:
            kol_dop_ras_0 = kol_ost_ras_0_2

        print('--- 2 ---')
        # проход по короткой стороне
        ras_1 = (lis_siz[0]//x[1])*(lis_siz[1]//x[0])
        ras_ost_1 = [[lis_siz[0] % x[1], lis_siz[1]], [lis_siz[1] % x[0], lis_siz[0]]]
        print(f'[[{lis_siz[0]} % {x[1]}, {lis_siz[1]}], [{lis_siz[1]} % {x[0]}, {lis_siz[0]}]]')
        print(f'[[{lis_siz[0] % x[1]}, {lis_siz[1]}], [{lis_siz[1] % x[0]}, {lis_siz[0]}]]')

        for j in range(4):
            kol_ost_ras_1_1 = (ras_ost_1[0][0] // x[1]) + (ras_ost_1[0][1] // x[0])
        kol_ost_ras_1_2 = (ras_ost_1[0][0] // x[0]) + (ras_ost_1[0][1] // x[1])

        print(kol_ost_ras_1_1, kol_ost_ras_1_2)

        if kol_ost_ras_1_1 > kol_ost_ras_1_2:
            kol_dop_ras_1 = kol_ost_ras_1_1
        else:
            kol_dop_ras_1 = kol_ost_ras_1_2

        # добавление количества с листа
        if ras_0 >= ras_1:
            if ras_0 >= kol_lis:
                kol_lis = ras_0 + kol_dop_ras_0
                var = x
        else:
            if ras_1 >= kol_lis:
                kol_lis = ras_1 + kol_dop_ras_1
                var = x

    result = 1 / kol_lis
    return [result, var, kol_lis]"""


def calc_lis(lis, lis_siz):
    """ проход по стороне lis_size[0] """
    ras = (lis_siz[0] // lis[0]) * (lis_siz[1] // lis[1])
    return ras


def calc_xy(lis, lis_siz):
    # проход по длинной стороне
    ras_0 = calc_lis(lis, lis_siz)
    ost_0 = lis_siz[0] - ((lis_siz[0] // lis[0]) * lis[0])
    ost_1 = lis_siz[1] - ((lis_siz[1] // lis[1]) * lis[1])

    if ost_0 > lis[1]:
        ras_ost_0 = calc_lis(lis, [ost_0, lis_siz[1]])
    else:
        ras_ost_0 = 0

    if ost_1 > lis[0]:
        ras_ost_1 = calc_lis(lis, [ost_1, lis_siz[0]])
    else:
        ras_ost_1 = 0

    return ras_0 + ras_ost_0 + ras_ost_1


def calc(lis, lis_siz):
    lis = lis[0]

    kol_lis_x = calc_xy(lis, lis_siz)

    # разворот заготовки на 90 градусов
    lis = [lis[1], lis[0]]

    kol_lis_y = calc_xy(lis, lis_siz)

    if kol_lis_x < kol_lis_y:
        kol_lis = kol_lis_y
        var = 1
    else:
        kol_lis = kol_lis_x
        var = 0

    result = 1 / kol_lis
    return [result, var, kol_lis]

