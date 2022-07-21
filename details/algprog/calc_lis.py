def calc(lis, lis_siz):
    kol_lis = 0
    var = None
    for x in lis:
        # проход по длинной стороне
        ras_0 = (lis_siz[0]//x[0])*(lis_siz[1]//x[1])
        ras_ost_0 = [[lis_siz[0] % x[0], lis_siz[1]], [lis_siz[1] % x[1], lis_siz[0]]]
        kol_ost_ras_0_1 = (ras_ost_0[0][0] // x[1]) * (ras_ost_0[0][1] // x[0])
        kol_ost_ras_0_2 = (ras_ost_0[0][0] // x[0]) * (ras_ost_0[0][1] // x[1])

        if kol_ost_ras_0_1 > kol_ost_ras_0_2:
            kol_dop_ras_0 = kol_ost_ras_0_1
        else:
            kol_dop_ras_0 = kol_ost_ras_0_2

        # проход по короткой стороне
        ras_1 = (lis_siz[0]//x[1])*(lis_siz[1]//x[0])
        ras_ost_1 = [[lis_siz[0] % x[1], lis_siz[1]], [lis_siz[1] % x[0], lis_siz[0]]]
        kol_ost_ras_1_1 = (ras_ost_1[0][0] // x[1]) * (ras_ost_1[0][1] // x[0])
        kol_ost_ras_1_2 = (ras_ost_1[0][0] // x[0]) * (ras_ost_1[0][1] // x[1])

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
    return [result, var]


