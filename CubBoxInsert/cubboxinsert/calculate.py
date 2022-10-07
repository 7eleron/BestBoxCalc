import numpy as np
from details.algprog.cal_m2 import calc_m2
from details.algprog.calc_lis import calc
from details.algprog.round import rou
from details.tray.tray_flat_cardboard import expence_cd
from details.tray.tray_paper_cross import expence_pap, tray_paper_once
from details.tray.tray_paper_rim import tray_paper_rim, tray_paper_rim_tw


class Box:
    def __init__(self, width, length, tray_hight, insert_hight, thickness_cb, lid_hight=30):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.insert_hight = insert_hight
        self.thickness_cb = thickness_cb
        self.lid_hight = lid_hight


class CardboardCubBoxInsert(Box):
    def cardboard_box(self, lis_siz):
        width_lt = self.width + (self.thickness_cb * 2)
        length_lt = self.length + (self.thickness_cb * 2)
        cardboard_lid = expence_cd(width_lt, length_lt, self.lid_hight, lis_siz)
        cardboard_tray = expence_cd(width_lt, length_lt, self.tray_hight, lis_siz)
        cardboard_insert = expence_cd(self.width, self.length, self.insert_hight, lis_siz)
        cardboard_result = cardboard_lid['Расход'] + cardboard_tray['Расход'] + cardboard_insert['Расход']
        return {'Расход': rou(cardboard_result),
                'Информация': f'Картон крышка - {cardboard_lid["Информация"]}'
                              f'Картон дно - {cardboard_tray["Информация"]}'
                              f'Картон вставка - {cardboard_insert["Информация"]}',
                'lid_tray_insert': (cardboard_lid['Расход'], cardboard_tray['Расход'],
                                    cardboard_insert['Расход'])
                }


class PaperBoxInsert(Box):
    def lid(self, lis_siz):
        width_lt = self.width + (self.thickness_cb * 2)
        length_lt = self.length + (self.thickness_cb * 2)
        paper_lid = expence_pap(width_lt, length_lt, self.lid_hight, self.thickness_cb, lis_siz)
        return {'Расход': paper_lid['Расход'],
                'Информация': f'Бумага крышка - {paper_lid["Информация"]}',
                'm2': paper_lid['m2']}

    # Дно в ручную
    def paper_tray_hand(self, lis_siz):
        width_lt = self.width + (self.thickness_cb * 2)
        length_lt = self.length + (self.thickness_cb * 2)
        if self.tray_hight <= 75:
            # бумага дно одним листом
            tray_pap = tray_paper_once(width_lt, length_lt, self.tray_hight, self.thickness_cb)
        else:
            # бумага дно бортом
            tray_pap = tray_paper_rim(width_lt, length_lt, self.tray_hight, self.thickness_cb)
            # бумага двумя бортами
            if tray_pap[0][1] > lis_siz[0]:
                tray_pap = tray_paper_rim_tw(width_lt, length_lt, self.tray_hight, self.thickness_cb)
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
        width_lt = self.width + (self.thickness_cb * 2)
        length_lt = self.length + (self.thickness_cb * 2)
        tray = tray_paper_once(width_lt, length_lt, self.tray_hight, self.thickness_cb)
        tray_ras = calc([tray], lis_siz)
        tray_m2 = calc_m2(tray)
        return {'Расход': tray_ras[0],
                'Информация': f'Бумага дно - {int(tray[0])}x{int(tray[1])}мм. ',
                'm2': tray_m2}

    def insert(self, lis_siz):
        paper_insert = expence_pap(self.width, self.length, self.insert_hight, self.thickness_cb, lis_siz)
        return {'Расход': paper_insert['Расход'],
                'Информация': f'Бумага вставка - {paper_insert["Информация"]}',
                'm2': paper_insert['m2']}
