import math
import numpy as np
from details.algprog.round import rou
from details.valvebends.valve import valve_tray
from details.algprog.calc_lis import calc
from details.algprog.cal_m2 import calc_m2


# бумага дно бортом
def tray_paper_rim(width, length, tray_hight, thickness_cb):
    indent = 5
    c = math.sqrt((thickness_cb ** 2) + (thickness_cb ** 2))
    corner = thickness_cb ** 4
    width_r = tray_hight + valve_tray() + c + thickness_cb + 10 + indent
    length_r = (width * 2) + (length * 2) + corner + valve_tray() + indent
    return [[math.ceil(width_r), math.ceil(length_r)], [width - 3, length - 3]]


# бумага дно двумя бортами
def tray_paper_rim_tw(width, length, tray_hight, thickness_cb):
    indent = 5
    c = math.sqrt((thickness_cb ** 2) + (thickness_cb ** 2))
    corner = thickness_cb ** 4
    width_r = tray_hight + valve_tray() + c + thickness_cb + 10 + indent
    length_r = width + length + (corner / 2) + valve_tray() + indent
    return [[math.ceil(width_r), math.ceil(length_r)], [width - 3, length - 3], [0, 0]]


# расход материала
def expence(tray, lis_siz):
    a = np.size(tray)
    if a == 4:
        tray_bor = calc([tray[0]], lis_siz)
        tray_dno = calc([tray[1]], lis_siz)
        tray_ras = tray_bor[0] + tray_dno[0]
        trayD_m2 = calc_m2(tray[1])
        trayB_m2 = calc_m2(tray[0])
        return {'Расход': rou(tray_ras),
                'Информация': f'лоток бортом. '\
                              f'Борт - {tray[0][0]}x{tray[0][1]}мм. Дно - {tray[1][0]}x{tray[1][1]}мм.',
                'm2': trayB_m2+trayD_m2}
    elif a == 6:
        tray_bor = calc([tray[0]], lis_siz) * 2
        tray_dno = calc([tray[1]], lis_siz)
        tray_ras = tray_bor[0] + tray_dno[0]
        trayD_m2 = calc_m2(tray[1])
        trayB_m2 = calc_m2(tray[0])*2
        return {'Расход': rou(tray_ras),
                'Информация': f'лоток двумя бортами. '\
                              f'Борт(х2) - {tray[0][0]}x{tray[0][1]}мм. Дно - {tray[1][0]}x{tray[1][1]}мм.',
                'm2': trayB_m2 + trayD_m2}


def expence_pap(width, length, tray_hight, thickness_cb, lis_siz):
    # бумага дно бортом
    tray_pap = tray_paper_rim(width, length, tray_hight, thickness_cb)
    # бумага двумя бортами
    if tray_pap[0][1] > lis_siz[0]:
        tray_pap = tray_paper_rim_tw(width, length, tray_hight, thickness_cb)
    result = expence(tray_pap, lis_siz)
    return result
