import numpy as np
from details.algprog.calc_lis import calc
from details.algprog.toFix import toFixed
from details.algprog.cal_m2 import calc_m2
from details.lid.lid_flat_cardboard import lid_cb
from details.lid.lid_paper_cross import lid_paper
from details.tray.tray_flat_cardboard import tray_cb
from details.tray.tray_paper_cross import tray_paper_once
from details.tray.tray_paper_rim import tray_paper_rim, tray_paper_rim_tw


class Cardboard_Box:
    def __init__(self, width, length, tray_hight, thickness_cb, lid_hight=30):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb
        self.lid_hight = lid_hight

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
        lid_card = lid_cb(self.width, self.length, self.lid_hight, self.thickness_cb)
        # развернутое дно
        tray_card = tray_cb(self.width, self.length, self.tray_hight)

        try:
            result = self.expence(lid_card, tray_card, lis_siz)

            return result
        except ZeroDivisionError:
            return 'Неполучилось разместить на листе.'


class Paper_Box_Hand:
    def __init__(self, width, length, tray_hight, thickness_cb, lid_hight=30):

        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb
        self.lid_hight = lid_hight

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
        lid_pap = lid_paper(self.width, self.length, self.lid_hight, self.thickness_cb)
        if self.tray_hight <= 75:
            # бумага дно одним листом
            tray_pap = tray_paper_once(self.width, self.length, self.tray_hight, self.thickness_cb)
        else:
            # бумага дно бортом
            tray_pap = tray_paper_rim(self.width, self.length, self.tray_hight, self.thickness_cb)
            # бумага двумя бортами
            if tray_pap[0][1] > lis_siz[0]:
                tray_pap = tray_paper_rim_tw(self.width, self.length, self.tray_hight, self.thickness_cb)

        try:
            result = self.expence(lid_pap, tray_pap, lis_siz)
            return result

        except ZeroDivisionError:
            return 'Неполучилось расчитать.'


class Paper_Box_Auto:
    def __init__(self, width, length, tray_hight, thickness_cb, lid_hight=30):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb
        self.lid_hight = lid_hight

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
        lid_pap = lid_paper(self.width, self.length, self.lid_hight, self.thickness_cb)
        tray_pap = tray_paper_once(self.width, self.length, self.tray_hight, self.thickness_cb)

        try:
            result = self.expence(lid_pap, tray_pap, lis_siz)
            return result

        except ZeroDivisionError:
            return 'Неполучилось расчитать.'