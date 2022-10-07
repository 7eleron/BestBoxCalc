import numpy as np
from details.algprog.calc_lis import calc
from details.algprog.cal_m2 import calc_m2
from details.algprog.round import rou
from details.lid.lid_flat_cardboard import lid_cb
from details.lid.lid_paper_cross import lid_paper
from details.tray.tray_flat_cardboard import tray_cb
from details.tray.tray_paper_cross import tray_paper_once
from details.tray.tray_paper_rim import tray_paper_rim, tray_paper_rim_tw


class Box:
    def __init__(self, width, length, tray_hight, thickness_cb, lid_hight=30):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb
        self.lid_hight = lid_hight


class CardboardBox(Box):
    def cardboard_box(self, lis_siz):
        # развернутая крышка
        lid_card = lid_cb(self.width, self.length, self.lid_hight, self.thickness_cb)
        # развернутое дно
        tray_card = tray_cb(self.width, self.length, self.tray_hight)

        ras_lid = calc([lid_card], lis_siz)
        ras_tray = calc([tray_card], lis_siz)

        result = ras_lid[0] + ras_tray[0]
        return {'Расход': rou(result),
                'Информация': f'Картон крышка - {int(lid_card[0])}x{int(lid_card[1])}мм. '
                              f'Картон дно - {int(tray_card[0])}x{int(tray_card[1])}мм. ',
                'lid_tray': (ras_lid[0], ras_tray[0])
                }


class PaperBox(Box):
    # Крышка
    def lid(self, lis_siz):
        lid = lid_paper(self.width, self.length, self.lid_hight, self.thickness_cb)
        lid_ras = calc([lid], lis_siz)
        lid_m2 = calc_m2(lid)
        return {'Расход': lid_ras[0],
                'Информация': f'Бумага крышка - {int(lid[0])}x{int(lid[1])}мм. ',
                'm2': lid_m2}

    # Дно в ручную
    def paper_tray_hand(self, lis_siz):
        if self.tray_hight <= 75:
            # бумага дно одним листом
            tray_pap = tray_paper_once(self.width, self.length, self.tray_hight, self.thickness_cb)
        else:
            # бумага дно бортом
            tray_pap = tray_paper_rim(self.width, self.length, self.tray_hight, self.thickness_cb)
            # бумага двумя бортами
            if tray_pap[0][1] > lis_siz[0]:
                tray_pap = tray_paper_rim_tw(self.width, self.length, self.tray_hight, self.thickness_cb)
        tray = tray_pap
        # результат дно и крышка раздельно
        a = np.size(tray)
        if a == 4:
            tray_bor = calc([tray[0]], lis_siz)
            tray_dno = calc([tray[1]], lis_siz)
            tray_ras = tray_bor[0] + tray_dno[0]
            trayD_m2 = calc_m2(tray[1])
            trayB_m2 = calc_m2(tray[0])
            return {'Расход': tray_ras,
                    'Информация': f'Бумага борт дна - {int(tray[0][0])}x{int(tray[0][1])}мм. '
                                  f'Бумага шлепок дна - {int(tray[1][0])}x{int(tray[1][1])}мм. ',
                    'm2': trayB_m2 + trayD_m2}

        elif a == 6:
            tray_bor = calc([tray[0]], lis_siz) * 2
            tray_dno = calc([tray[1]], lis_siz)
            tray_ras = tray_bor[0] + tray_dno[0]
            trayD_m2 = calc_m2(tray[1])
            trayB_m2 = calc_m2(tray[0]) * 2
            return {'Расход': tray_ras,
                    'Информация': f'Бумага борт дна(х2) - {int(tray[0][0])}x{int(tray[0][1])}мм. '
                                  f'Бумага шлепок дна - {int(tray[1][0])}x{int(tray[1][1])}мм. ',
                    'm2': trayB_m2 + trayD_m2}
        else:
            tray_ras = calc([tray], lis_siz)[0]
            tray_m2 = calc_m2(tray)
            return {'Расход': tray_ras,
                    'Информация': f'Бумага дно - {int(tray[0])}x{int(tray[1])}мм. ',
                    'm2': tray_m2}

    # Дно автомат
    def paper_tray_auto(self, lis_siz):
        tray = tray_paper_once(self.width, self.length, self.tray_hight, self.thickness_cb)
        tray_ras = calc([tray], lis_siz)
        tray_m2 = calc_m2(tray)
        return {'Расход': tray_ras[0],
                'Информация': f'Бумага дно - {int(tray[0])}x{int(tray[1])}мм. ',
                'm2': tray_m2}
