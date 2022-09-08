from cub_box_0.models import Work


def laminating_work(expense):
    price = Work.objects.get(Name='кашировка').Lid
    return price*expense
