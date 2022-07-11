from django.shortcuts import render
from cub_box.result import result_data_box
from casket.result import result_data_casket
from alg_prog.currency import currency_eur


# Create your views here.
def first_page(request):
    cur_euro = currency_eur()
    return render(request, './index.html', {'cur_euro': cur_euro})


def req_data(request):

    try:
        cur_euro = currency_eur()
        construction = request.POST['construction']

        if construction == 'Крышка-дно':
            a, b, c = int(request.POST['width']), int(request.POST['length']), int(request.POST['hight'])
            cardboard_req = request.POST['cardboard']
            paper_req = request.POST['paper']
            kol = int(request.POST['kol'])
            lid_hight = int(request.POST['lid_hight'])
            result = result_data_box(a, b, c, cardboard_req, paper_req, kol, lid_hight)
            construction = 'Крышка-дно'

        elif construction == 'Шкатулка':
            a, b, c = int(request.POST['width']), int(request.POST['length']), int(request.POST['hight'])
            cardboard_req = request.POST['cardboard']
            paper_req = request.POST['paper']
            kol = int(request.POST['kol'])
            result = result_data_casket(a, b, c, cardboard_req, paper_req, kol)
            construction = 'Шкатулка'

        return render(request, './result.html', {'construction': construction, 'result': result, 'cur_euro': cur_euro})

    except Exception as ex:
        return render(request, './result.html', {'ex': ex})

