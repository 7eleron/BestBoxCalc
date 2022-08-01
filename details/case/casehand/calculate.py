from details.case.case_cardboard import expence_case_cb
from details.case.case_paper import expence_pap_case


class ExpenceCase:
    def __init__(self, width, length, tray_hight, thickness_cb):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb

    def result(self, lis_siz):
        # внутренние размеры с учететом лотка
        width_c, length_c = self.width+((self.thickness_cb*2)+2), self.length+((self.thickness_cb*2)+1)
        hight = self.tray_hight+(self.thickness_cb+2)
        # расход материалов
        paper = expence_pap_case(width_c, hight, length_c, self.thickness_cb, lis_siz)
        cardboard = expence_case_cb(width_c, length_c, hight, lis_siz)
        return {'cardboard': cardboard, 'paper': paper}
