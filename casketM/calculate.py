from details.algprog.round import rou
from details.folderM.folder_cardboard import expence_fol_cb
from details.folderM.folder_paper import expence_pap_fold
from details.folderM.end_paper import expence_end_paper
from details.tray.tray_flat_cardboard import expence_cd
from details.tray.tray_paper_cross import expence_pap as expence_pap_tray
from details.tray.tray_paper_casket import expence_tray_casket


class Box:
    def __init__(self, width, length, tray_hight, thickness_cb):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb


class CardboardCasketBox(Box):
    def cardboard_box(self, lis_siz):
        cardboard_folder = expence_fol_cb(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        cardboard_tray = expence_cd(self.width, self.length, self.tray_hight, lis_siz)
        cardboard_result = cardboard_folder['Расход'] + cardboard_tray['Расход']
        return {'Расход': rou(cardboard_result),
                'Информация': f'Картон крышка(папка) - {cardboard_folder["Информация"]}'
                              f'Картон дно(крест) - {cardboard_tray["Информация"]}',
                'lid_tray': (cardboard_folder['Расход'], cardboard_tray['Расход'])
                }


class PaperCasketBox(Box):
    def lid(self, lis_siz):
        paper_folder = expence_pap_fold(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        paper_end = expence_end_paper(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        paper_result = paper_folder['Расход'] + paper_end['Расход']
        return {'Расход': rou(paper_result),
                'Информация': f'Бумага внешняя оклейка крышки(папки) - {paper_folder["Информация"]}'
                              f'Бумага внутренняя оклейка крышки(форзац) - {paper_end["Информация"]}',
                'm2': paper_folder['m2'] + paper_end['m2']}

    # Дно в ручную
    def paper_tray_hand(self, lis_siz):
        paper_tray = expence_tray_casket(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        return {'Расход': paper_tray['Расход'],
                'Информация': f'Бумага {paper_tray["Информация"]}мм. ',
                'm2': paper_tray['m2']}

    # Дно автомат
    def paper_tray_auto(self, lis_siz):
        paper_tray = expence_pap_tray(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        return {'Расход': paper_tray['Расход'],
                'Информация': f'Бумага внешняя оклейка дна - {paper_tray["Информация"]}мм. ',
                'm2': paper_tray['m2']}
