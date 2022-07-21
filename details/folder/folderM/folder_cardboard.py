from details.algprog.calc_lis import calc


# картонная папка
def folder_cb(width, length, tray_hight, thickness_cb):
    indent = 5
    width_r = width+(thickness_cb*5)+indent
    flap_length = (tray_hight+thickness_cb)+indent
    lid_length = length+(thickness_cb*2)+indent
    tray_length = length+(thickness_cb*3)+indent
    return [width_r, flap_length, flap_length, lid_length, tray_length]


# расход материала
def expence_fol_cb(width, length, hight, thickness_cb, lis_siz):
    folder = folder_cb(width, length, hight, thickness_cb)
    folder_exp = 0
    for dit in folder[1:]:
        folder_exp += calc([[folder[0], dit]], lis_siz)[0]
    return {'Расход': float(folder_exp),
            'Информация': folder}