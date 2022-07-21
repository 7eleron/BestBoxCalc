from cub_box_0.models import Work2


def hand_work(a, b, hight):
    object_list = Work2.objects.all()
    size_box = a+b
    work_count = None
    for obj in object_list:
        if size_box <= obj.Size and hight <= obj.Hight:
            work_count = obj.Count
            break
    return work_count