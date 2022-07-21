from django.shortcuts import render
from cubbox.result import result_data_box
from casketM.result import result_data_casket
from details.tray.trayauto.result import result_data_tray_auto
from details.algprog.currency import currency_eur


# Create your views here.
def first_page(request):
    cur_euro = currency_eur()
    return render(request, './index.html', {'cur_euro': cur_euro})


def req_data(request):

    #try:
        cur_euro = currency_eur()
        construction = request.POST['construction']
        a, b, c = int(request.POST['width']), int(request.POST['length']), int(request.POST['hight'])
        kol = int(request.POST['kol'])
        cardboard_req = request.POST['cardboard']
        paper_req = request.POST['paper']

        if construction == 'Крышка-дно':
            lid_hight = int(request.POST['lid_hight'])
            result = result_data_box(a, b, c, cardboard_req, paper_req, kol, lid_hight)
            construction = 'Крышка-дно'

        elif construction == 'Шкатулка':
            result = result_data_casket(a, b, c, cardboard_req, paper_req, kol)
            construction = 'Шкатулка'

        elif construction == 'Лоток':
            result = result_data_tray_auto(a, b, c, cardboard_req, paper_req)
            construction = 'Лоток'

        return render(request, './result.html', {'construction': construction,
                                                 'cur_euro': cur_euro,
                                                 'info': result.get('Информация о коробке'),
                                                 'expence': result.get('Расходы'),
                                                 'work': result.get('Работа'),
                                                 'prices': result.get('Цены'),
                                                 'priceshtamp': result.get('Цена штампа')})

    #except Exception as ex:
        return render(request, './result.html', {'ex': ex})

