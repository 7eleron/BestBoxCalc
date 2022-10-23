import math
from cub_box_0.models import Material


def plywood_detail(width, length, thickness_plywood: int, number: int = 1):
    outline = (((width * 2) + (length * 2)) / 1000 + 1.3) * number
    square = (width * length) / 1000000
    plywood = Material.objects.get(mt_name='Фанера', len=thickness_plywood)
    cost_plywood = math.ceil((square * 1.5 * plywood.size_x + outline * 90) / 50) * 50
    if cost_plywood < plywood.size_y:
        cost_plywood = plywood.size_y
    return cost_plywood


def mold(width, length, height):
    price = 0
    all_detail = {8: 2}
    top_detail_number_dict = {}
    for x in Material.objects.filter(mt_name='Фанера'):
        if height / x.len:
            top_detail_number_dict[int(x.len)] = height // x.len
    top_detail_number = {6: top_detail_number_dict[6]}
    for i in top_detail_number_dict:
        if top_detail_number_dict.get(i) < list(top_detail_number.keys())[0]:
            top_detail_number = {i: top_detail_number_dict.get(i)}
    all_detail[list(top_detail_number.keys())[0]] = top_detail_number.get(list(top_detail_number.keys())[0])
    residual = height - list(top_detail_number.keys())[0] * top_detail_number.get(list(top_detail_number.keys())[0])
    for j in Material.objects.filter(mt_name='Фанера'):
        if j.len > residual:
            if j.len in all_detail:
                all_detail[j.len] += 1
            else:
                all_detail[j.len] = 1
            break
    for k in list(all_detail.keys()):
        price += plywood_detail(width=width, length=length,
                                thickness_plywood=k, number=all_detail.get(k))
    return price
