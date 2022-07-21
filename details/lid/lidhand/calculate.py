from details.tray.tray_flat_cardboard import expence_cd
from details.tray.tray_paper_cross import expence_pap


class ExpenceLid:
    def __init__(self, width, length, hight, thickness_cb):
        self.width = width + (thickness_cb*2) + 2
        self.length = length + (thickness_cb*2) + 2
        self.hight = hight
        self.thickness_cb = thickness_cb

    def result(self, lis_siz):
        try:
            cardboard = expence_cd(self.width, self.length, self.hight, lis_siz)
            paper = expence_pap(self.width, self.length, self.hight, self.thickness_cb, lis_siz)
            return {'cardboard': cardboard, 'paper': paper}
        except ZeroDivisionError:
            return 'Неполучилось расчитать.'
        except Exception as ex:
            return ex
