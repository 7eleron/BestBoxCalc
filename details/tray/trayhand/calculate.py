from details.tray.tray_flat_cardboard import expence_cd
from details.tray.tray_paper_rim import expence_pap
from details.tray.tray_paper_cross import expence_pap as expence_pap_once


class ExpenceTray:
    def __init__(self, width, length, tray_hight, thickness_cb):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb

    def result(self, lis_siz):
        try:
            cardboard = expence_cd(self.width, self.length, self.tray_hight, lis_siz)
            if self.tray_hight >= 75:
                paper = expence_pap(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
            else:
                paper = expence_pap_once(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)

            return {'cardboard': cardboard, 'paper': paper}
        except ZeroDivisionError:
            return 'Неполучилось расчитать.'
        except Exception as ex:
            return ex
