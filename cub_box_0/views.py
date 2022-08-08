from django.shortcuts import render
from details.algprog.currency import currency_eur
from cms.models import CmsSlider
from cub_box_0.models import Material
from services.resp_result import responseresult
from services.req_constructions import request_construction_cubbox, request_construction_cubboxinsert
from services.req_constructions import request_construction_case, request_construction_casketm
from services.req_constructions import request_construction_briefcase


def material():
    cardboard_list = [x for x in Material.objects.all() if x.mt_type == 'картон']
    paper_list = [x for x in Material.objects.all() if x.mt_type == 'дизайнерская бумага']
    return {'cardboard_list': cardboard_list, 'paper_list': paper_list}


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
        return render(request, f'./cubbox.html', material() | responseresult(result))
    except:
        return render(request, './cubbox.html', material() | {'cur_euro': currency_eur(),
                                                     'ex': ''})


def cubboxinsert_page(request):
    try:
        result = request_construction_cubboxinsert(request)
        return render(request, './cubboxinsert.html', material() | responseresult(result))
    except:
        return render(request, './cubboxinsert.html', material() | {'cur_euro': currency_eur(),
                                                     'ex': ''})


def case_page(request):
    try:
        result = request_construction_case(request)
        return render(request, './case.html', material() | responseresult(result))
    except:
        return render(request, './case.html', material() | {'cur_euro': currency_eur(),
                                                     'ex': ''})


def casketm_page(request):
    try:
        result = request_construction_casketm(request)
        return render(request, './casketm.html', material() | responseresult(result))
    except:
        return render(request, './casketm.html', material() | {'cur_euro': currency_eur(),
                                                     'ex': ''})


def briefcase_page(request):
    handle = {'handle': [x for x in Material.objects.all() if x.mt_type == 'ручка']}
    try:
        result = request_construction_briefcase(request)
        return render(request, './briefcase.html', handle | material() | responseresult(result))
    except:
        return render(request, './briefcase.html', handle | material() | {'cur_euro': currency_eur(),
                                                     'ex': ''})
