from django.shortcuts import render
from details.algprog.currency import currency_eur
from cms.models import CmsSlider
from services.resp_result import responseresult
from services.req_constructions import request_construction_cubbox, request_construction_cubboxinsert
from services.req_constructions import request_construction_case, request_construction_casketm


# Create your views here.
def first_page(request):
    slider_list = CmsSlider.objects.all()
    try:
        return render(request, './index.html', {'slider_list': slider_list})
    except:
        return render(request, './index.html', {'slider_list': slider_list, 'ex': ''})


def cubbox_page(request):
    try:
        result = request_construction_cubbox(request)
        return render(request, f'./cubbox.html', responseresult(result))
    except:
        return render(request, './cubbox.html', {'cur_euro': currency_eur(),
                                                 'ex': ''})


def cubboxinsert_page(request):
    try:
        result = request_construction_cubboxinsert(request)
        return render(request, './cubboxinsert.html', responseresult(result))
    except:
        return render(request, './cubboxinsert.html', {'cur_euro': currency_eur(),
                                                     'ex': ''})


def case_page(request):
    try:
        result = request_construction_case(request)
        return render(request, './case.html', responseresult(result))
    except:
        return render(request, './case.html', {'cur_euro': currency_eur(),
                                                     'ex': ''})


def casketm_page(request):
    try:
        result = request_construction_casketm(request)
        return render(request, './casketm.html', responseresult(result))
    except:
        return render(request, './casketm.html', {'cur_euro': currency_eur(),
                                                     'ex': ''})
