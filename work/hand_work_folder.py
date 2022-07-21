from cub_box_0.models import Work


def folder_work(m2, type_work):
    object = Work.objects.get(Name=type_work).Lid
    return object * m2