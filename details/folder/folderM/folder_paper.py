import math
from details.valvebends.valve import valve_folder
from details.algprog.calc_lis import calc
from details.algprog.toFix import toFixed
from details.algprog.cal_m2 import calc_m2


# бумага папка одним
def folder_paper_one(width, length, hight, thickness_cb):
    indent = 5
    width_r = width + (thickness_cb * 5) + (valve_folder()*2) + indent
    flap_length = (hight + thickness_cb)
    lid_length = length + (thickness_cb * 2)
    tray_length = length + (thickness_cb * 3)
    length_r = (flap_length * 2) + lid_length + tray_length + (thickness_cb * 6) + (valve_folder()*2) + indent
    return [math.ceil(width_r), math.ceil(length_r)]


# бумага папка двумя
def folder_paper_dab(width, length, hight, thickness_cb):
    indent = 5
    width_r = width + (thickness_cb * 5) + (valve_folder()*2) + indent
    flap_length = (hight + thickness_cb)
    lid_length = length + (thickness_cb * 2)
    tray_length = length + (thickness_cb * 3)
    length_first = valve_folder() + flap_length + lid_length + (thickness_cb * 4) + 30 + indent
    length_sec = flap_length + tray_length + (thickness_cb * 2) + valve_folder() + indent
    first_fold = [width_r, length_first]
    sec_fild = [width_r, length_sec]
    return [first_fold, sec_fild]


# расход материала
def expence_pap_fold(width, length, hight, thickness_cb, lis_siz):
    try:
        folder = folder_paper_one(width, length, hight, thickness_cb)
        fold_ras = calc([folder], lis_siz)
        fold_m2 = calc_m2(folder)
        return {'Расход': float(toFixed(fold_ras[0], 2)),
                'Информация': f'{folder[0]}x{folder[1]}мм.',
                'm2': fold_m2}
    except ZeroDivisionError:
        folder = folder_paper_dab(width, length, hight, thickness_cb)
        fold_ras = calc([folder[0]], lis_siz)[0] + calc([folder[1]], lis_siz)[0]
        fold_m2 = calc_m2(folder[0]) + calc_m2(folder[1])
        return {'Расход': float(toFixed(fold_ras, 2)),
                'Информация': f'Папка 1 - {folder[0][0]}x{folder[0][1]}мм.'\
                              f'Папка 2 - {folder[1][0]}x{folder[1][1]}мм.',
                'm2': fold_m2}
    except Exception as ex:
        return ex