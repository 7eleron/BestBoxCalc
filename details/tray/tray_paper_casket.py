import math
from details.valvebends.valve import valve_casket
from details.algprog.calc_lis import calc
from details.algprog.cal_m2 import calc_m2


# бумага дно бортом
def tray_paper_rim_one(width, length, hight, thickness_cb):
    indent = 5
    corner = (thickness_cb * 2) * 3
    width_r = valve_casket() + hight + 10 + indent
    length_r = valve_casket() + width + (length * 2) + valve_casket() + corner + indent
    return [math.ceil(width_r), math.ceil(length_r)]


# бумага дно двумя бортами
def tray_paper_rim_tw(width, length, hight, thickness_cb):
    indent = 5
    corner = thickness_cb * 2
    width_r = valve_casket() + hight + 10 + indent
    length_fir = valve_casket() + length + width + (corner * 2) + valve_casket() + indent
    length_sec = length + corner + valve_casket() + indent
    return [[math.ceil(width_r), math.ceil(length_fir)], [math.ceil(width), math.ceil(length_sec)]]


# расход материала
def expence_tray_casket(width, length, hight, thickness_cb, lis_siz):
    try:
        tray = tray_paper_rim_one(width, length, hight, thickness_cb)
        tray_ras = calc([tray], lis_siz)
        tray_m2 = calc_m2(tray)
        return {'Расход': float(tray_ras[0]),
                'Информация': f'одним бортом {tray[0]}x{tray[1]}мм. ',
                'm2': tray_m2}
    except ZeroDivisionError:
        tray = tray_paper_rim_tw(width, length, hight, thickness_cb)
        tray_ras = calc([tray[0]], lis_siz)[0] + calc([tray[1]], lis_siz)[0]
        tray_m2 = calc_m2(tray[0]) + calc_m2(tray[1])
        return {'Расход': float(tray_ras),
                'Информация': f'двумя бортами. '
                              f'Борт 1 - {tray[0][0]}x{tray[0][1]}мм. '\
                              f'Борт 2 - {tray[1][0]}x{tray[1][1]}мм. ',
                'm2': tray_m2}
    except Exception as ex:
        return ex