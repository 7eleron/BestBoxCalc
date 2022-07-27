import math
import numpy as np
from details.valvebends.valve import valve_case
from details.algprog.calc_lis import calc
from details.algprog.cal_m2 import calc_m2
from details.algprog.toFix import toFixed


# бумага футляр бортом
def paper_rim(width, length, tray_hight, thickness_cb):
    indent = 5
    c = math.sqrt((thickness_cb ** 2) + (thickness_cb ** 2))
    corner = thickness_cb ** 4
    width_r = tray_hight + valve_case() + c + thickness_cb + 10 + indent
    length_r = (width * 2) + (length * 2) + corner + valve_case() + indent
    return [[math.ceil(width_r), math.ceil(length_r)], [width - 3, length - 3]]


# бумага футляр двумя бортами
def paper_rim_tw(width, length, tray_hight, thickness_cb):
    indent = 5
    c = math.sqrt((thickness_cb ** 2) + (thickness_cb ** 2))
    corner = thickness_cb ** 4
    width_r = tray_hight + valve_case() + c + thickness_cb + 10 + indent
    length_r = width + length + (corner / 2) + valve_case() + indent
    return [[math.ceil(width_r), math.ceil(length_r)], [width - 3, length - 3], [0, 0]]


# расход материала
def expence(case, lis_siz):
    a = np.size(case)
    if a == 4:
        tray_bor = calc([case[0]], lis_siz)
        tray_dno = calc([case[1]], lis_siz)
        tray_ras = tray_bor[0] + tray_dno[0]
        trayD_m2 = calc_m2(case[1])
        trayB_m2 = calc_m2(case[0])
        return {'Расход': float(toFixed(tray_ras, 2)),
                'Информация': f'Одним бортом. ' \
                              f'Борт - {case[0][0]}x{case[0][1]}мм. Дно - {case[1][0]}x{case[1][1]}мм.',
                'm2': trayB_m2 + trayD_m2}
    elif a == 6:
        tray_bor = calc([case[0]], lis_siz) * 2
        tray_dno = calc([case[1]], lis_siz)
        tray_ras = tray_bor[0] + tray_dno[0]
        trayD_m2 = calc_m2(case[1])
        trayB_m2 = calc_m2(case[0]) * 2
        print(f'Двумя бортами. ' \
              f'Борт(х2) - {case[0][0]}x{case[0][1]}мм. Дно - {case[1][0]}x{case[1][1]}мм.')
        return {'Расход': float(toFixed(tray_ras, 2)),
                'Информация': f'Двумя бортами. ' \
                              f'Борт(х2) - {case[0][0]}x{case[0][1]}мм. Дно - {case[1][0]}x{case[1][1]}мм.',
                'm2': trayB_m2 + trayD_m2}


def expence_pap_case(width, length, tray_hight, thickness_cb, lis_siz):
    # бумага бортом
    tray_pap = paper_rim(width, length, tray_hight, thickness_cb)
    # бумага двумя бортами
    if tray_pap[0][1] > lis_siz[0]:
        tray_pap = paper_rim_tw(width, length, tray_hight, thickness_cb)

    try:
        result = expence(tray_pap, lis_siz)
        return result

    except ZeroDivisionError:
        return 'Неполучилось расчитать.'
