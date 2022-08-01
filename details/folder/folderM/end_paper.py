import math
from details.algprog.calc_lis import calc
from details.algprog.cal_m2 import calc_m2
from details.algprog.round import rou


# бумага форзац
def end_paper(width, length, hight, thickness_cb):
    indent = 5
    width_r = width + (thickness_cb * 4) + indent
    flap_length = (hight + thickness_cb)
    lid_length = length + (thickness_cb * 2)
    length_r = flap_length + lid_length + (thickness_cb * 4) + 20 + indent
    return [math.ceil(width_r), math.ceil(length_r)]


# расход материала
def expence_end_paper(width, length, hight, thickness_cb, lis_siz):
    end_pap = end_paper(width, length, hight, thickness_cb)
    end_pap_ras = calc([end_pap], lis_siz)
    end_pap_m2 = calc_m2(end_pap)
    return {'Расход': rou(end_pap_ras[0]),
            'Информация': f'форзац {end_pap[0]}x{end_pap[1]}мм. ',
            'm2': end_pap_m2}
