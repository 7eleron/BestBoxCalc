import numpy as np
from details.algprog.cal_m2 import calc_m2
from details.algprog.calc_lis import calc
from details.case.case_cardboard import expence_case_cb
from details.case.case_paper import expence_pap_case
from details.tray.tray_flat_cardboard import expence_cd
from details.tray.tray_paper_cross import expence_pap
from details.tray.tray_paper_rim import tray_paper_rim, tray_paper_rim_tw


class Box:
    def __init__(self, width, length, tray_hight, thickness_cb):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb


class CardboardCaseBox(Box):
    def cardboard_box(self, lis_siz):
        width_c, length_c = self.width + ((self.thickness_cb * 2) + 2), self.length + ((self.thickness_cb * 2) + 1)
        hight = self.tray_hight + (self.thickness_cb + 2)
        cardboard_case = expence_case_cb(width_c, length_c, hight, lis_siz)
        cardboard_tray = expence_cd(self.width, self.length, self.tray_hight, lis_siz)
        cardboard_result = cardboard_case['Расход'] + cardboard_tray['Расход']
        return {'Расход': cardboard_result,
                'Информация': f'Картон шубер - {cardboard_case["Информация"]}'
                              f'Картон дно - {cardboard_tray["Информация"]}',
                'lid_tray': (cardboard_case['Расход'], cardboard_tray['Расход'])
                }


class PaperCaseBox(Box):
    def lid(self, lis_siz):
        # внутренние размеры футляра с учететом лотка
        width_c, length_c = self.width + ((self.thickness_cb * 2) + 2), self.length + ((self.thickness_cb * 2) + 1)
        hight = self.tray_hight + (self.thickness_cb + 2)
        paper_case = expence_pap_case(width_c, hight, length_c, self.thickness_cb, lis_siz)
        return {'Расход': paper_case['Расход'],
                'Информация': f'Бумага футляр - {paper_case["Информация"]}',
                'm2': paper_case['m2']}

    # Дно в ручную
    def paper_tray_hand(self, lis_siz):
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

        else:
            tray_bor = calc([tray[0]], lis_siz) * 2
            tray_dno = calc([tray[1]], lis_siz)
            tray_ras = tray_bor[0] + tray_dno[0]
            trayD_m2 = calc_m2(tray[1])
            trayB_m2 = calc_m2(tray[0]) * 2
            return {'Расход': tray_ras,
                    'Информация': f'Бумага борт дна(х2) - {int(tray[0][0])}x{int(tray[0][1])}мм. '
                                  f'Бумага шлепок дна - {int(tray[1][0])}x{int(tray[1][1])}мм. ',
                    'm2': trayB_m2 + trayD_m2}

    # Дно автомат
    def paper_tray_auto(self, lis_siz):
        paper_tray = expence_pap(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        return {'Расход': paper_tray['Расход'],
                'Информация': f'Бумага дно - {paper_tray["Информация"]}мм. ',
                'm2': paper_tray['m2']}
