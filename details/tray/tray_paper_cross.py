import math
from algprog.calc_lis import calc
from algprog.toFix import toFixed
from algprog.cal_m2 import calc_m2


# бумага дно одним листом
def tray_paper_once(width, length, hight, thickness_cb):
    indent = 5
    c = math.sqrt((thickness_cb ** 2) + (thickness_cb ** 2))
    width = (hight*2)+width+(thickness_cb*2)+(c*2)+(15*2)+indent
    length = (hight*2)+length+(thickness_cb*2)+(c*2)+(15*2)+indent
    return [math.ceil(width), math.ceil(length)]


# расход материала
def expence_pap(width, length, hight, thickness_cb, lis_siz):
    tray = tray_paper_once(width, length, hight, thickness_cb)
    tray_ras = calc([tray], lis_siz)
    tray_m2 = calc_m2(tray)
    return {'Расход': float(toFixed(tray_ras[0], 2)),
            'Информация': f'{tray[0]}x{tray[1]}мм.',
            'm2': tray_m2}