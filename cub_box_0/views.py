from django.shortcuts import render
from .models import Work, Material, calc_count, Work2
from .calculate import Cardboard_Box, Paper_Box_Hand, Paper_Box_Auto
from .currency import currency_eur as cur_euro
from .shtamp import cutter


# Create your views here.
def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def first_page(request):
    return render(request, './index.html', {'cur_euro': cur_euro})


def machin_work(res_paper, kol):
    object_list = Work.objects.all()
    for obj in object_list:
        if obj.Name == 'крышка_авто' and obj.dm2 <= res_paper[2]:
            lid = ((obj.Content + obj.Scotch) + (obj.Close_fitting / kol)) + obj.Lid
        elif obj.Name == 'дно_авто' and obj.dm2 <= res_paper[3]:
            tray = ((obj.Content + obj.Scotch) + (obj.Close_fitting / kol)) + obj.Tray
    return [lid, tray]


def hand_work(a, b, hight):
    object_list = Work2.objects.all()
    size_box = a+b
    work_count = None
    for obj in object_list:
        if size_box <= obj.Size and hight <= obj.Hight:
            work_count = obj.Count
            break
    return work_count


def req_data(request):
    try:
        a, b, c = int(request.POST['width']), int(request.POST['length']), int(request.POST['hight'])
        cardboard_req = request.POST['cardboard']
        paper_req = request.POST['paper']
        currency_req = cur_euro()
        kol = int(request.POST['kol'])
        lid_hight = int(request.POST['lid_hight'])
        thickness_cb = Material.objects.get(mt_name=cardboard_req).len
        lis_siz = [Material.objects.get(mt_name=cardboard_req).size_x, Material.objects.get(mt_name=cardboard_req).size_y]

        if kol >= 500 and a >= 80 and b >= 65 and c >= 10:
            if a <= 460 and b <= 380 and c <= 120:
                cardboard = Cardboard_Box(a, b, c, thickness_cb, lid_hight)
                result_cardboard = cardboard.cardboard_box(lis_siz=lis_siz)
                paper = Paper_Box_Auto(a, b, c, thickness_cb, lid_hight)
                result_paper = paper.cub_box_paper(lis_siz=lis_siz)
                lid = machin_work(result_paper, kol)[0]
                tray = machin_work(result_paper, kol)[1]
                work = lid+tray
                shtamp_res = cutter(a, b, c, lid_hight)*2
                type_work = ['Сборка автоматическая.', 'machin']

            else:
                cardboard = Cardboard_Box(a, b, c, thickness_cb, lid_hight)
                result_cardboard = cardboard.cardboard_box(lis_siz=lis_siz)
                paper = Paper_Box_Hand(a, b, c, thickness_cb, lid_hight)
                result_paper = paper.cub_box_paper(lis_siz=lis_siz)
                work = hand_work(a, b, c)
                shtamp_res = cutter(a, b, c, lid_hight)
                type_work = ['Сборка ручная.', 'hand']
        else:
            cardboard = Cardboard_Box(a, b, c, thickness_cb, lid_hight)
            result_cardboard = cardboard.cardboard_box(lis_siz=lis_siz)
            paper = Paper_Box_Hand(a, b, c, thickness_cb, lid_hight)
            result_paper = paper.cub_box_paper(lis_siz=lis_siz)
            work = hand_work(a, b, c)
            shtamp_res = cutter(a, b, c, lid_hight)
            type_work = ['Сборка ручная.', 'hand']

        currency = {'euro': currency_req, 'rub': 1}

        data_calc = calc_count.objects.get(style_work=type_work[1])
        paper_obj = Material.objects.get(mt_name= paper_req)
        paper_count = (paper_obj.prise * (currency.get(paper_obj.currency))*float(result_paper[0]))
        cardboard_obj = Material.objects.get(mt_name= cardboard_req)

        cardboard_count = (cardboard_obj.prise * (currency.get(cardboard_obj.currency))*float(result_cardboard[0]))
        production_cost = (paper_count+cardboard_count)*data_calc.reject+data_calc.cut+(work)+((work)\
                                                                            *data_calc.not_production)
        calc_sum = ((production_cost*data_calc.margin)*data_calc.manager_proc)+production_cost

        data = f'Размер коробки {a}x{b}x{c}мм. Высота крышки {lid_hight}. Картон {thickness_cb}мм. Тираж {kol}шт.'
        return render(request, './result.html', {'data': data,
                                                 'result_cardboard_0': result_cardboard[0],
                                                 'result_cardboard_1': result_cardboard[1],
                                                 'result_paper_0': result_paper[0], 'result_paper_1': result_paper[1],
                                                 'work': work, 'type_work': type_work[0],
                                                 'cardboard': cardboard_req, 'paper': paper_req,
                                                 'sum': toFixed(calc_sum, 2),
                                                 'cur_euro': cur_euro, 'shtamp': toFixed(shtamp_res, 2)})
    except Exception as ex:
        return render(request, './result.html', {'ex': ex})

