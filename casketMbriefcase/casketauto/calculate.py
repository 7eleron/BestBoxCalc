from details.folderM.folder_cardboard import expence_fol_cb
from details.folderM.folder_paper import expence_pap_fold
from details.folderM.end_paper import expence_end_paper
from details.tray.tray_flat_cardboard import expence_cd
from details.tray.tray_paper_cross import expence_pap as expence_pap_tray


class ExpenceCasket:
    def __init__(self, width, length, tray_hight, thickness_cb):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb

    def result(self, lis_siz):
        # расход картона
        cardboard_folder = expence_fol_cb(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        cardboard_tray = expence_cd(self.width, self.length, self.tray_hight, lis_siz)
        cardboard_result = cardboard_folder['Расход'] + cardboard_tray['Расход']
        cardboard_info = ('папка ' + cardboard_folder['Информация']) \
                         + ('лоток ' + cardboard_tray['Информация'])
        cardboard = {'Расход': cardboard_result,
                     'Информация': cardboard_info}
        # расход бумаги
        paper_folder = expence_pap_fold(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        paper_end = expence_end_paper(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        paper_tray = expence_pap_tray(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        paper_result = paper_folder['Расход'] + paper_end['Расход'] + paper_tray['Расход']
        paper_info = ('папка ' + paper_folder['Информация']) \
                  + ('форзац ' + paper_end['Информация'])\
                   + ('лоток ' + paper_tray['Информация'])
        m2 = {
            'крышка': paper_folder['m2']+paper_end['m2'],
            'дно': paper_tray['m2']}
        paper = {'Расход': paper_result,
                 'Информация': paper_info,
                 'm2': m2
                 }
        return {'cardboard': cardboard, 'paper': paper}
