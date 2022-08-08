from details.tray.tray_flat_cardboard import expence_cd
from details.tray.tray_paper_rim import expence_pap as expence_pap_rim
from details.tray.tray_paper_cross import expence_pap
from CubBoxInsert.cubboxinsert.inssert_paper import expence_pap_insert


class ExpenceCubBoxInsert:
    def __init__(self, width, length, tray_hight, lid_hight, insert_hight, thickness_cb):
        self.width = width
        self.length = length
        self.lid_hight = lid_hight
        self.tray_hight = tray_hight
        self.insert_hight = insert_hight
        self.thickness_cb = thickness_cb

    def result(self, lis_siz):
        width_lt = self.width + (self.thickness_cb * 2)
        length_lt = self.length + (self.thickness_cb * 2)
        cardboard_lid = expence_cd(width_lt, length_lt, self.lid_hight, lis_siz)
        cardboard_tray = expence_cd(width_lt, length_lt, self.tray_hight, lis_siz)
        cardboard_insert = expence_cd(self.width, self.length, self.insert_hight, lis_siz)
        cardboard_result = cardboard_lid['Расход']+cardboard_tray['Расход']+cardboard_insert['Расход']
        cardboard_info = ('крышка '+cardboard_lid['Информация'])\
                         +('донышко '+cardboard_tray['Информация'])\
                         +('вставка '+cardboard_insert['Информация'])
        cardboard = {'Расход': cardboard_result,
                     'Информация': cardboard_info
                     }
        paper_lid = expence_pap(width_lt, length_lt, self.tray_hight, self.thickness_cb, lis_siz)
        paper_tray = expence_pap_rim(width_lt, length_lt, self.tray_hight, self.thickness_cb, lis_siz)

        if self.insert_hight <= 80:
            paper_insert = expence_pap(self.width, self.length, self.insert_hight, self.thickness_cb, lis_siz)
        else:
            paper_insert = expence_pap_insert(self.width, self.length, self.tray_hight, self.insert_hight,
                                              self.thickness_cb, lis_siz)

        paper_result = paper_lid['Расход'] + paper_tray['Расход'] + paper_insert['Расход']
        paper_info = ('крышка ' + paper_lid['Информация']) \
                      + ('донышко ' + paper_tray['Информация']) \
                      + (' вставка ' + paper_insert['Информация'])
        m2 = {
            'крышка': paper_lid['m2'],
            'дно': paper_tray['m2'],
            'вставка': paper_insert['m2']
        }
        paper = {'Расход': paper_result,
                 'Информация': paper_info,
                 'm2': m2
                 }

        return {'cardboard': cardboard, 'paper': paper}
