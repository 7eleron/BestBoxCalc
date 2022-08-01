from details.folder.folderM.folder_cardboard import expence_fol_cb
from details.folder.folderM.folder_paper import expence_pap_fold
from details.folder.folderM.end_paper import expence_end_paper


class ExpenceFolder:
    def __init__(self, width, length, tray_hight, thickness_cb):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb

    def result(self, lis_siz):
        cardboard = expence_fol_cb(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        paper_folder = expence_pap_fold(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        paper_end = expence_end_paper(self.width, self.length, self.tray_hight, self.thickness_cb, lis_siz)
        return {'cardboard': cardboard, 'paper_folder': paper_folder, 'paper_end': paper_end}
