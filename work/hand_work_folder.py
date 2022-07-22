from cub_box_0.models import Work


def folder_work(m2):
    objects = Work.objects.all()
    lid = None
    for obj in objects:
        if obj.Name == 'папка ручная' and obj.dm2 <= m2:
            lid = obj.Lid
    return lid
