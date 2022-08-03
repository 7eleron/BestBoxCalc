from details.algprog.calc_lis import calc


# картонное дно
def tray_cb(width, length, hight):
    indent = 5
    width = (hight*2)+width+indent
    length = (hight*2)+length+indent
    return [width, length]


# расход материала
def expence_cd(width, length, hight, lis_siz):
    tray = tray_cb(width, length, hight)
    tray_exp = calc([tray], lis_siz)[0]
    return {'Расход': float(tray_exp),
            'Информация': f'{tray[0]}x{tray[1]}мм. '}
