from django.shortcuts import render
from cubbox.result import result_data_box
from casketM.result import result_data_casket
from Case.result import result_data_case
from CubBoxInsert.result import result_data_cdinsert
from details.algprog.currency import currency_eur


# Create your views here.
def first_page(request):
    return render(request, './index.html', {'cur_euro': currency_eur()})


def request_construction(a, b, c, cardboard_req, paper_req, kol, lid_hight, construction, cur_euro):
    if construction == 'Крышка-дно':
        result = result_data_box(a, b, c, cardboard_req, paper_req, kol, lid_hight, cur_euro)
        return result
    elif construction == 'Крышка-дно со вставкой':
        result = result_data_cdinsert(a, b, c, cardboard_req, paper_req, kol, lid_hight, cur_euro)
        return result
    elif construction == 'Пенал':
        result = result_data_case(a, b, c, cardboard_req, paper_req, kol, cur_euro)
        return result
    elif construction == 'Шкатулка на магнитах':
        result = result_data_casket(a, b, c, cardboard_req, paper_req, kol, cur_euro)
        return result


def req_data(request):
    #try:
        req_cur_euro = request.POST['currency'].strip().split(',')
        cur_euro = 0
        if len(req_cur_euro) == 1:
            cur_euro = float(req_cur_euro[0])
        elif len(req_cur_euro) == 2:
            cur_euro = float(req_cur_euro[0] + '.' + req_cur_euro[1])

        construction = request.POST['construction']
        cardboard_req = request.POST['cardboard']
        paper_req = request.POST['paper']
        a, b, c = int(request.POST['width'].strip()), int(request.POST['length'].strip()), int(request.POST['hight'].strip())
        kol = int(request.POST['kol'].strip())
        lid_hight = int(request.POST['lid_hight'].strip())
        result = request_construction(a, b, c, cardboard_req, paper_req, kol, lid_hight, construction, cur_euro)

        return render(request, './result.html', {'construction': construction,
                                                 'cur_euro': currency_eur(),
                                                 'sen_cur_euro': cur_euro,
                                                 'info': result.get('Информация о коробке'),
                                                 'expence': result.get('Расходы'),
                                                 'work': result.get('Работа'),
                                                 'prices': result.get('Цены'),
                                                 'priceshtamp': result.get('Цена штампа'),
                                                 'infocb': result.get('Информация картон'),
                                                 'infotpap': result.get('Информация бумага'),
                                                 })
    #except ValueError:
        return render(request, './result.html', {'cur_euro': currency_eur(), 'ex': 'Введите числовые данные.'})

    #except ZeroDivisionError:
        return render(request, './result.html', {'cur_euro': currency_eur(), 'ex': 'Размер требует расчета в ручную.'})

    #except TypeError:
        return render(request, './result.html', {'cur_euro': currency_eur(), 'ex': 'Размер требует расчета в ручную.'})

    #except AttributeError:
        return render(request, './result.html', {'cur_euro': currency_eur(), 'ex': 'Размер требует расчета в ручную.'})

    #except Exception:
        return render(request, './result.html', {'cur_euro': currency_eur(), 'ex': ''})
