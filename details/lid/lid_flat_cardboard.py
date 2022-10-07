from details.algprog.calc_lis import calc


# картонная крышка
def lid_cb(width, length, lid_hight, thickness_cb):
    indent = 5
    width = (lid_hight*2)+width+(thickness_cb*2)+2+indent
    length = (lid_hight*2)+length+(thickness_cb*2)+2+indent
    return [width, length]


# расход материала
def expence_pap(width, length, hight, thickness_cb, lis_siz):
    lid = lid_cb(width, length, hight, thickness_cb)
    lid_ras = calc([lid], lis_siz)
    return {'Расход': float(lid_ras[0]),
            'Информация': f'{lid[0]}x{lid[1]}мм.'}
