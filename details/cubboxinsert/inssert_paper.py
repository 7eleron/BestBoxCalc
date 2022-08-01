import math
from details.algprog.round import rou
from details.valvebends.valve import valve_insert
from details.algprog.calc_lis import calc
from details.algprog.cal_m2 import calc_m2


# бумага вставка бортом
def paper_rim(width, length, tray_hight, insert_hight, thickness_cb):
    indent = 5
    corner = thickness_cb ** 4
    width_r = (insert_hight-tray_hight) + (valve_insert()*2) + thickness_cb + indent
    length_r = (width * 2) + (length * 2) + corner + valve_insert() + indent
    return [math.ceil(width_r), math.ceil(length_r)]


# бумага футляр двумя бортами
def paper_rim_tw(width, length, tray_hight, insert_hight, thickness_cb):
    indent = 5
    corner = thickness_cb ** 4
    width_r = (insert_hight-tray_hight) + (valve_insert()*2) + thickness_cb + indent
    length_r = (width + length) + (corner/2) + valve_insert() + indent
    return [math.ceil(width_r), math.ceil(length_r)]


# расход материала
def expence_pap_insert(width, length, tray_hight, insert_hight, thickness_cb, lis_siz):
    # бумага бортом
    try:
        insert_pap = paper_rim(width, length, tray_hight, insert_hight, thickness_cb)
        insert_ras = calc([insert_pap], lis_siz)[0]
        insert_m2 = calc_m2(insert_pap)
        return {'Расход': rou(insert_ras),
                'Информация': f'одной полосой. ' \
                              f'Полоса - {insert_pap[0]}x{insert_pap[1]}мм. ',
                'm2': insert_m2}

    # бумага двумя бортами
    except ZeroDivisionError:
        insert_pap = paper_rim_tw(width, length, tray_hight, insert_hight, thickness_cb)
        insert_ras = calc([insert_pap], lis_siz)[0] * 2
        insert_m2 = calc_m2(insert_pap) * 2
        return {'Расход': rou(insert_ras),
                'Информация': f'двумя полосами. '
                              f'Полоса(х2) - {insert_pap[0]}x{insert_pap[1]}мм. ',
                'm2': insert_m2}
