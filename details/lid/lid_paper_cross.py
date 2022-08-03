import math
from details.valvebends.valve import valve_lid
from details.algprog.calc_lis import calc
from details.algprog.cal_m2 import calc_m2


# бумага крышка
def lid_paper(width, length, lid_hight, thickness_cb):
    indent = 5
    c = math.sqrt((thickness_cb ** 2) + (thickness_cb ** 2))
    width_r = (lid_hight*2)+width+(thickness_cb*2)+1+(c*2)+(valve_lid()*2)+indent
    length_r = (lid_hight*2)+length+(thickness_cb*2)+1+(c*2)+(valve_lid()*2)+indent
    return [math.ceil(width_r), math.ceil(length_r)]


# расход материала
def expence_pap(width, length, hight, thickness_cb, lis_siz):
    lid = lid_paper(width, length, hight, thickness_cb)
    lid_ras = calc([lid], lis_siz)
    lid_m2 = calc_m2(lid)
    return {'Расход': float(lid_ras[0]),
            'Информация': f'{lid[0]}x{lid[1]}мм.',
            'm2': lid_m2}