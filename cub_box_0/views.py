from django.shortcuts import render
from cubbox.result import result_data_box
from casketM.result import result_data_casket
from details.tray.trayauto.result import result_data_tray_auto
from details.algprog.currency import currency_eur


# Create your views here.
def first_page(request):
    cur_euro = currency_eur()
    return render(request, './index.html', {'cur_euro': cur_euro})


def request_construction(a, b, c, cardboard_req, paper_req, kol, lid_hight, construction):
    if construction == 'Крышка-дно':
        result = result_data_box(a, b, c, cardboard_req, paper_req, kol, lid_hight)
        return result
    elif construction == 'Шкатулка':
        result = result_data_casket(a, b, c, cardboard_req, paper_req, kol)
        return result
    elif construction == 'Лоток':
        result = result_data_tray_auto(a, b, c, cardboard_req, paper_req)
        return result


def req_data(request):
    if str(currency_eur()).isdigit():
        cur_euro = 60
    else:
        cur_euro = currency_eur()

    try:
        construction = request.POST['construction']
        cardboard_req = request.POST['cardboard']
        paper_req = request.POST['paper']
        try:
            a, b, c = int(request.POST['width'].strip()), int(request.POST['length'].strip()), int(request.POST['hight'].strip())
            kol = int(request.POST['kol'].strip())
            lid_hight = int(request.POST['lid_hight'].strip())
            result = request_construction(a, b, c, cardboard_req, paper_req, kol, lid_hight, construction)

            return render(request, './result.html', {'construction': construction,
                                                     'cur_euro': cur_euro,
                                                     'info': result.get('Информация о коробке'),
                                                     'expence': result.get('Расходы'),
                                                     'work': result.get('Работа'),
                                                     'prices': result.get('Цены'),
                                                     'priceshtamp': result.get('Цена штампа')})

        except ValueError:
            return render(request, './result.html', {'cur_euro': cur_euro, 'info': 'Введите числовые данные.'})

    except Exception as ex:
        return render(request, './result.html', {'cur_euro': cur_euro, 'ex': ex})

