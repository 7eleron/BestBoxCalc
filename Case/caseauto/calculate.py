from details.case.case_cardboard import expence_case_cb
from details.case.case_paper import expence_pap_case
from details.tray.tray_flat_cardboard import expence_cd
from details.tray.tray_paper_cross import expence_pap


class ExpenceCase:
    def __init__(self, width, length, tray_hight, thickness_cb):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb

    def result(self, lis_siz):
        # внутренние размеры футляра с учететом лотка
        width_c, length_c = self.width + ((self.thickness_cb * 2) + 2), self.length + ((self.thickness_cb * 2) + 1)
        hight = self.tray_hight + (self.thickness_cb + 2)

        # расход картона
        cardboard_case = expence_case_cb(width_c, length_c, hight, lis_siz)
        cardboard_tray = expence_cd(self.width, self.length, self.tray_hight, lis_siz)
        cardboard_result = cardboard_case['Расход']+cardboard_tray['Расход']
        cardboard_info = ('футляр '+cardboard_case['Информация'])\
                         +('лоток '+cardboard_tray['Информация'])
        cardboard = {'Расход': cardboard_result,
                     'Информация': cardboard_info}

        # расход бумаги
        paper_case = expence_pap_case(width_c, length_c, hight, self.thickness_cb, lis_siz)
        paper_tray = expence_pap(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        paper_result = paper_case['Расход'] + paper_tray['Расход']
        paper_info = ('футляр ' + paper_case['Информация']) \
                      + ('лоток ' + paper_tray['Информация'])
        m2 = {
            'крышка': paper_case['m2'],
            'дно': paper_tray['m2']}
        paper = {'Расход': paper_result,
                 'Информация': paper_info,
                 'm2': m2
                 }

        return {'cardboard': cardboard, 'paper': paper}
