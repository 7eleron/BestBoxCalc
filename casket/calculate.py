import math
from alg_prog.calc_lis import calc
from alg_prog.toFix import toFixed
from alg_prog.cal_m2 import calc_m2


class Cardboard_Casket:
    def __init__(self, width, length, tray_hight, thickness_cb):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb

    # картонная папка
    def folder_cb(self):
        indent = 5
        width = self.width+(self.thickness_cb*5)+indent
        flap_length = (self.tray_hight+self.thickness_cb)+indent
        lid_length = self.length+(self.thickness_cb*2)+indent
        tray_length = self.length+(self.thickness_cb*3)+indent
        return [width, flap_length, flap_length, lid_length, tray_length]

    # картонное дно
    def tray_cb(self):
        indent = 10
        width = (self.tray_hight*2)+self.width+indent
        length = (self.tray_hight*2)+self.length+indent
        return [width, length]

    # расход материала
    def expence(self, lis_siz):
        folder = self.folder_cb()
        tray = self.tray_cb()
        folder_exp = 0
        for dit in folder[1:]:
            folder_exp += calc([[folder[0], dit]], lis_siz)[0]
        tray_exp = calc([tray], lis_siz)[0]
        return folder_exp + tray_exp

    def cardboard_casket(self, lis_siz):
        try:
            result = self.expence(lis_siz)
            return result
        except ZeroDivisionError:
            return 'Неполучилось разместить на листе.'


class Paper_Casket:
    def __init__(self, width, length, tray_hight, thickness_cb):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb

    # бумага папка одним
    def folder_paper_one(self):
        indent = 5
        width = self.width + (self.thickness_cb * 5) + 40 + indent
        flap_length = (self.tray_hight + self.thickness_cb)
        lid_length = self.length + (self.thickness_cb * 2)
        tray_length = self.length + (self.thickness_cb * 3)
        length = (flap_length*2)+lid_length+tray_length+(self.thickness_cb*6)+40+indent
        return [math.ceil(width), math.ceil(length)]

    # бумага папка двумя
    def folder_paper_dab(self):
        indent = 5
        width = self.width + (self.thickness_cb * 5) + 40 + indent
        flap_length = (self.tray_hight + self.thickness_cb)
        lid_length = self.length + (self.thickness_cb * 2)
        tray_length = self.length + (self.thickness_cb * 3)
        length_first = 20 + flap_length + lid_length + (self.thickness_cb * 4) + 30 + indent
        length_sec = flap_length + tray_length + (self.thickness_cb * 2) + 20 + indent
        first_fold = [width, length_first]
        sec_fild = [width, length_sec]
        return [first_fold, sec_fild]

    # бумага форзац
    def end_paper(self):
        indent = 5
        width = self.width + (self.thickness_cb * 4) + indent
        flap_length = (self.tray_hight + self.thickness_cb)
        lid_length = self.length + (self.thickness_cb * 2)
        length = flap_length + lid_length + (self.thickness_cb * 4) + 20 + indent
        return [math.ceil(width), math.ceil(length)]

    # бумага дно одним листом
    def tray_paper_once(self):
        indent = 5
        c = math.sqrt((self.thickness_cb ** 2) + (self.thickness_cb ** 2))
        width = (self.tray_hight*2)+self.width+(self.thickness_cb*2)+(c*2)+(20*2)+indent
        length = (self.tray_hight*2)+self.length+(self.thickness_cb*2)+(c*2)+(20*2)+indent
        return [math.ceil(width), math.ceil(length)]

    # бумага дно бортом
    def tray_paper_rim_one(self):
        indent = 5
        corner = (self.thickness_cb * 2) * 3
        width = 20 + self.tray_hight + 10 + indent
        length = 20 + self.width + (self.length * 2) + 20 + corner + indent
        return [math.ceil(width), math.ceil(length)]

    # бумага дно двумя бортами
    def tray_paper_rim_tw(self):
        indent = 5
        corner = self.thickness_cb * 2
        width = 20 + self.tray_hight + 10 + indent
        length_fir = 20 + self.length + self.width + (corner * 2) + 20 + indent
        length_sec = self.length + corner + 20 + indent
        return [[math.ceil(width), math.ceil(length_fir)], [math.ceil(width), math.ceil(length_sec)]]

    # расход материала
    def expence(self, lis_siz, type_work):
        try:
            # результат папка одним листом
            folder = self.folder_paper_one()
            folder_ras = calc([folder], lis_siz)
            folder_m2 = calc_m2(folder)
            endpaper = self.end_paper()
            endpaper_ras = calc([endpaper], lis_siz)
            endpaper_m2 = calc_m2(endpaper)

            if type_work == 'шкатулка автомат':
                # результат дно для машинки
                tray = self.tray_paper_once()
                tray_ras = calc([tray], lis_siz)
                tray_m2 = calc_m2(tray)
                return {'except': toFixed(folder_ras[0] + tray_ras[0] + endpaper_ras[0], 2),
                        'info': f'Папка одним листом. Лоток на автомате. '
                                f'Папка - {folder[0]}x{folder[1]}мм. '
                                f'Форзац - {endpaper[0]}x{endpaper[1]}мм. '
                                f'Лоток - {tray[0]}x{tray[1]}мм.',
                        'm2': [folder_m2, tray_m2, endpaper_m2]}

            else:
                # результат дно в ручную одним
                try:
                    tray = self.tray_paper_rim_one()
                    tray_ras = calc([tray], lis_siz)
                    tray_m2 = calc_m2(tray)
                    return {'except': toFixed(folder_ras[0] + tray_ras[0] + endpaper_ras[0], 2),
                            'info': f'Папка одним листом. Лоток в ручную, борт одним листом. '
                                    f'Форзац - {endpaper[0]}x{endpaper[1]}мм. '
                                    f'Папка - {folder[0]}x{folder[1]}мм. '
                                    f'Борт - {tray[0]}x{tray[1]}мм.',
                            'm2': [folder_m2, tray_m2, endpaper_m2]}
                # результат дно в ручную двумя
                except ZeroDivisionError:
                    tray = self.tray_paper_rim_tw()
                    tray_ras = calc([tray[0]], lis_siz)+calc([tray[1]], lis_siz)
                    tray_m2 = calc_m2(tray[0]) + calc_m2(tray[1])
                    return {'except': toFixed(folder_ras[0] + tray_ras[0] + endpaper_ras[0], 2),
                            'info': f'Папка одним листом. Лоток в ручную, борт одним листом. '
                                    f'Папка - {folder[0]}x{folder[0]}мм. '
                                    f'Форзац - {endpaper[0]}x{endpaper[1]}мм. '
                                    f'Борт 1 - {tray[0][0]}x{tray[0][1]}мм. Борт 2 - {tray[1][0]}x{tray[1][1]}мм.',
                            'm2': [folder_m2, tray_m2, endpaper_m2]}

        except ZeroDivisionError:
            # результат папка двумя листами
            folder = self.folder_paper_dab()
            folder_ras = calc([folder[0]], lis_siz)+calc([folder[1]], lis_siz)
            folder_m2 = calc_m2(folder[0])+calc_m2(folder[1])
            endpaper = self.end_paper()
            endpaper_ras = calc([endpaper], lis_siz)
            endpaper_m2 = calc_m2(endpaper)
            if type_work == 'шкатулка автомат':
                # результат дно для машинки
                tray = self.tray_paper_once()
                tray_ras = calc([tray], lis_siz)
                tray_m2 = calc_m2(tray)
                return {'except': toFixed(folder_ras[0] + tray_ras[0] + endpaper_ras[0], 2),
                        'info': f'Папка двумя листами. Лоток на автомате. '
                                f'Папка 1 - {folder[0][0]}x{folder[0][1]}мм. '
                                f'Папка 2 - {folder[1][0]}x{folder[1][1]}мм '
                                f'Форзац - {endpaper[0]}x{endpaper[1]}мм. '
                                f'Лоток - {tray[0]}x{[1]}мм.',
                        'm2': [folder_m2, tray_m2, endpaper_m2]}

            else:
                # результат дно в ручную одним
                try:
                    tray = self.tray_paper_rim_one()
                    tray_ras = calc([tray], lis_siz)
                    tray_m2 = calc_m2(tray)
                    return {'except': toFixed(folder_ras[0] + tray_ras[0] + endpaper_ras[0], 2),
                            'info': f'Папка двумя листами. Лоток в ручную, борт одним листом. '
                                    f'Папка 1 - {folder[0][0]}x{folder[0][1]}мм. '
                                    f'Папка 2 - {folder[1][0]}x{folder[1][1]}мм '
                                    f'Форзац - {endpaper[0]}x{endpaper[1]}мм. '
                                    f'Борт - {tray[0]}x{[1]}мм.',
                            'm2': [folder_m2, tray_m2, endpaper_m2]}
                # результат дно в ручную двумя
                except ZeroDivisionError:
                    tray = self.tray_paper_rim_tw()
                    tray_ras = calc([tray[0]], lis_siz)+calc([tray[1]], lis_siz)
                    tray_m2 = calc_m2(tray[0])+calc_m2(tray[1])
                    return {'except': toFixed(folder_ras[0] + tray_ras[0] + endpaper_ras[0], 2),
                            'info': f'Папка двумя листами. Лоток в ручную, борт одним листом. '
                                    f'Папка 1 - {folder[0][0]}x{folder[0][1]}мм. '
                                    f'Папка 2 - {folder[1][0]}x{folder[1][1]}мм '
                                    f'Форзац - {endpaper[0]}x{endpaper[1]}мм. '
                                    f'Борт 1 - {tray[0][0]}x{tray[0][1]}мм. Борт 2 - {tray[1][0]}x{tray[1][1]}мм.',
                            'm2': [folder_m2, tray_m2, endpaper_m2]}

    def paper_casket(self, lis_siz, type_work):
        try:
            result = self.expence(lis_siz, type_work)
            return result

        except ZeroDivisionError:
            return 'Неполучилось расчитать.'