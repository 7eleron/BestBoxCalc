import numpy as np
import math


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


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


def calc_m2(lis):
    m2 = (lis[0]/100) * (lis[1]/100)
    return m2


class Cardboard_Box:
    def __init__(self, width, length, tray_hight, thickness_cb, lid_hight=30):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb
        self.lid_hight = lid_hight

    # картонная крышка
    def lid_cb(self):
        indent = 5
        width = (self.lid_hight*2)+self.width+(self.thickness_cb*2)+2+indent
        length = (self.lid_hight*2)+self.length+(self.thickness_cb*2)+2+indent
        return [width, length]

    # картонное дно
    def tray_cb(self):
        indent = 10
        width = (self.tray_hight*2)+self.width+indent
        length = (self.tray_hight*2)+self.length+indent
        return [width, length]

    # расчет отдельно крышка и дно
    def sep_lid_tray(self, lid, tray, lis_siz):
        # проверка крышки
        ras_lid = calc([lid], lis_siz)

        # проверка дна
        ras_tray = calc([tray], lis_siz)

        result = ras_lid[0] + ras_tray[0]
        return result

    # расход материала
    def expence(self, lid, tray, lis_siz):
        lis_one = [lid, tray]
        try:
            # четыре варианта располодения крышки и дно вместе
            if tray[0] >= lid[0]:
                tray_lid_1 = tray[0]
            else:
                tray_lid_1 = lid[0]

            if tray[0] >= lid[1]:
                tray_lid_2 = tray[0]
            else:
                tray_lid_2 = lid[1]

            if tray[1] >= lid[1]:
                tray_lid_4 = tray[1]
            else:
                tray_lid_4 = lid[1]

            if tray[1] <= lid[0]:
                tray_lid_3 = lid[0]
            else:
                tray_lid_3 = tray[1]

            lis_tw = [[tray_lid_1, lid[1] + tray[1]], [tray[0] + lid[0], tray_lid_4],
                      [tray_lid_2, lid[0] + tray[1]], [lid[1] + tray[0], tray_lid_3]]

            # результат дно и крышка вместе
            result_tw = calc(lis_tw, lis_siz)
            # результат дно и крышка раздельно
            result_one = self.sep_lid_tray(lid, tray, lis_siz)

            if result_tw[0] <= result_one:
                return [toFixed(result_tw[0], 2),
                        f'Крышка и дно вместе. Крышка-дно - {result_tw[1][0]}x{result_tw[1][1]}мм.']
            else:
                return [toFixed(result_one, 2),
                        f'Крышка и дно раздельно. Крышка - {lis_one[0][0]}x{lis_one[0][1]}мм. '
                        f'Дно - {lis_one[1][0]}x{lis_one[1][1]}мм.']

        except ZeroDivisionError:
            result = self.sep_lid_tray(lid, tray, lis_siz)
            return [toFixed(result, 2),
                    f'Крышка и дно раздельно. Крышка - {lis_one[0][0]}x{lis_one[0][1]}мм. '
                    f'Дно - {lis_one[1][0]}x{lis_one[1][1]}мм.']

    def cardboard_box(self, lis_siz):
        # развернутая крышка
        lid_card = self.lid_cb()
        # развернутое дно
        tray_card = self.tray_cb()

        try:
            result = self.expence(lid_card, tray_card, lis_siz)

            return result
        except ZeroDivisionError:
            return 'Неполучилось разместить на листе.'


class Paper_Box_Hand:
    def __init__(self, width, length, tray_hight, thickness_cb, lid_hight=30, kink_paper_lid=20, kink_paper_tray=20):

        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb
        self.lid_hight = lid_hight
        self.kink_paper_lid = kink_paper_lid
        self.kink_paper_tray = kink_paper_tray

    # бумага крышка
    def lid_paper(self):
        indent = 5
        c = math.sqrt((self.thickness_cb ** 2) + (self.thickness_cb ** 2))
        width = (self.lid_hight*2)+self.width+(self.thickness_cb*2)+1+(c * 2)+(self.kink_paper_lid*2)+indent
        length = (self.lid_hight*2)+self.length+(self.thickness_cb*2)+1+(c*2)+(self.kink_paper_lid*2)+indent
        return [math.ceil(width), math.ceil(length)]

    # бумага дно одним листом
    def tray_paper_once(self):
        indent = 5
        c = math.sqrt((self.thickness_cb ** 2) + (self.thickness_cb ** 2))
        width = (self.lid_hight*2)+self.width+(self.thickness_cb*2)+(c*2)+(self.kink_paper_tray*2)+indent
        length = (self.lid_hight*2)+self.length+(self.thickness_cb*2)+(c*2)+(self.kink_paper_tray*2)+indent
        return [math.ceil(width), math.ceil(length)]

    # бумага дно бортом
    def tray_paper_rim(self):
        indent = 5
        c = math.sqrt((self.thickness_cb ** 2) + (self.thickness_cb ** 2))
        corner = self.thickness_cb ** 4
        width = self.tray_hight + self.kink_paper_tray + c + self.thickness_cb + 10 + indent
        length = (self.width * 2) + (self.length * 2) + corner + 20 + indent
        return [[math.ceil(width), math.ceil(length)], [self.width - 3, self.length - 3]]

    # бумага дно двумя бортами
    def tray_paper_rim_tw(self):
        indent = 5
        c = math.sqrt((self.thickness_cb ** 2) + (self.thickness_cb ** 2))
        corner = self.thickness_cb ** 4
        width = self.tray_hight + self.kink_paper_tray + c + self.thickness_cb + 10 + indent
        length = self.width + self.length + (corner / 2) + 20 + indent
        return [[math.ceil(width), math.ceil(length)], [self.width - 3, self.length - 3], [0, 0]]

    # расход материала
    def expence(self, lid, tray, lis_siz):
        lis_one = [lid, tray]
        try:
            # результат дно и крышка вместе
            lid_ras = calc([lid], lis_siz)
            # результат дно и крышка раздельно
            a = np.size(tray)
            if a == 4:
                tray_bor = calc([tray[0]], lis_siz)
                tray_dno = calc([tray[1]], lis_siz)
                tray_ras = tray_bor[0] + tray_dno[0]
                lid_m2 = calc_m2(lid)
                trayD_m2 = calc_m2(tray[1])
                trayB_m2 = calc_m2(tray[0])
                return [toFixed(lid_ras[0] + tray_ras, 2), f'Донышко бортом. Крышка - {lid[0]}x{lid[1]}мм. '
                       f'Борт - {tray[0][0]}x{tray[0][1]}мм. Дно - {tray[1][0]}x{tray[1][1]}мм.',
                        lid_m2, trayB_m2+trayD_m2]
            elif a == 6:
                tray_bor = calc([tray[0]], lis_siz) * 2
                tray_dno = calc([tray[1]], lis_siz)
                tray_ras = tray_bor[0] + tray_dno[0]
                lid_m2 = calc_m2(lid)
                trayD_m2 = calc_m2(tray[1])
                trayB_m2 = calc_m2(tray[0])*2
                return [toFixed(lid_ras[0] + tray_ras, 2), f'Донышко бортом. Крышка - {lid[0]}x{lid[1]}мм. '
                        f'Борт(х2) - {tray[0][0]}x{tray[0][1]}мм. Дно - {tray[1][0]}x{tray[1][1]}мм.',
                        lid_m2, trayB_m2+trayD_m2]
            else:
                tray_ras = calc([tray], lis_siz)[0]
                lid_m2 = calc_m2(lid)
                tray_m2 = calc_m2(tray)
                return [toFixed(lid_ras[0] + tray_ras, 2), f'Донышко одним листом. Крышка - {lid[0]}x{lid[1]}мм. '
                                                           f'Дно - {tray[0]}x{tray[1]}мм.', lid_m2, tray_m2]
        except Exception:
            return Exception

    def cub_box_paper(self, lis_siz):
        # бумага крышка
        lid_pap = self.lid_paper()
        if self.tray_hight <= 75:
            # бумага дно одним листом
            tray_pap = self.tray_paper_once()
        else:
            # бумага дно бортом
            tray_pap = self.tray_paper_rim()
            # бумага двумя бортами
            if tray_pap[0][1] > lis_siz[0]:
                tray_pap = self.tray_paper_rim_tw()

        try:
            result = self.expence(lid_pap, tray_pap, lis_siz)
            return result

        except ZeroDivisionError:
            return 'Неполучилось расчитать.'


class Paper_Box_Auto:
    def __init__(self, width, length, tray_hight, thickness_cb, lid_hight=30, kink_paper_lid=20, kink_paper_tray=20):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb
        self.lid_hight = lid_hight
        self.kink_paper_lid = kink_paper_lid
        self.kink_paper_tray = kink_paper_tray

    # бумага крышка
    def lid_paper(self):
        indent = 5
        c = math.sqrt((self.thickness_cb ** 2) + (self.thickness_cb ** 2))
        width = (self.lid_hight*2)+self.width+(self.thickness_cb*2)+1+(c * 2)+(self.kink_paper_lid*2)+indent
        length = (self.lid_hight*2)+self.length+(self.thickness_cb*2)+1+(c*2)+(self.kink_paper_lid*2)+indent
        return [math.ceil(width), math.ceil(length)]

    # бумага дно одним листом
    def tray_paper_once(self):
        indent = 5
        c = math.sqrt((self.thickness_cb ** 2) + (self.thickness_cb ** 2))
        width = (self.lid_hight*2)+self.width+(self.thickness_cb*2)+(c*2)+(self.kink_paper_tray*2)+indent
        length = (self.lid_hight*2)+self.length+(self.thickness_cb*2)+(c*2)+(self.kink_paper_tray*2)+indent
        return [math.ceil(width), math.ceil(length)]

    # расход материала
    def expence(self, lid, tray, lis_siz):
        try:
            # результат дно и крышка вместе
            lid_ras = calc([lid], lis_siz)

            tray_ras = calc([tray], lis_siz)[0]
            lid_m2 = calc_m2(lid)
            tray_m2 = calc_m2(tray)
            return [toFixed(lid_ras[0] + tray_ras, 2), f'Донышко одним листом. Крышка - {lid[0]}x{lid[1]}мм. '
                                                           f'Дно - {tray[0]}x{tray[1]}мм.', lid_m2, tray_m2]
        except Exception:
            return Exception

    def cub_box_paper(self, lis_siz):
        # бумага крышка
        lid_pap = self.lid_paper()
        tray_pap = self.tray_paper_once()

        try:
            result = self.expence(lid_pap, tray_pap, lis_siz)
            return result

        except ZeroDivisionError:
            return 'Неполучилось расчитать.'
