from cub_box_0.models import Work


def machin_work_cubbox(res_paper):
    object_list = Work.objects.all()
    lid = None
    tray = None
    for obj in object_list:
        if obj.Name == 'крышка_авто' and obj.dm2 <= res_paper[0]:
            lid = obj.Lid
        elif obj.Name == 'дно_авто' and obj.dm2 <= res_paper[1]:
            tray = obj.Tray

    return lid+tray


def machin_work_tray(res_paper):
    object_list = Work.objects.all()
    tray = None
    for obj in object_list:
        if obj.Name == 'лоток автомат' and obj.dm2 <= res_paper:
            tray = obj.Tray

    return tray