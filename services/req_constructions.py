from cubbox.result import result_data_box
from casketM.result import result_data_casket
from casketMbriefcase.result import result_data_briefcase
from Case.result import result_data_case
from CubBoxInsert.result import result_data_cdinsert
from services.marga import pressfoil_calc, pattern_calc


def request_construction(request):
    req_cur_euro = request.POST['currency'].strip().split(',')
    cur_euro = 0
    if len(req_cur_euro) == 1:
        cur_euro = float(req_cur_euro[0])
    elif len(req_cur_euro) == 2:
        cur_euro = float(req_cur_euro[0] + '.' + req_cur_euro[1])
    cardboard_req = request.POST['cardboard']
    paper_req = request.POST['paper']
    lam_req_lid = request.POST['laminatinglid']
    lam_req_tray = request.POST['laminatingtray']
    lam_req = [lam_req_lid, lam_req_tray]
    a, b, c = int(request.POST['width'].strip()), int(request.POST['length'].strip()), int(
        request.POST['height'].strip())
    kol = int(request.POST['kol'].strip())
    lid_height = int(request.POST['lid_height'].strip())
    feature = {
        'pressfoil':  pressfoil_calc(request.POST['pressfoil'].strip().split(';'), kol),
        'pattern':  pattern_calc(request.POST['printing'].strip().split(';'), kol),
        'logement':  float(request.POST['logement'].strip()),
    }
    uppercost = float(request.POST['uppercost'].strip())
    return {
        'width': a, 'length': b, 'height': c,
        'cardboard': cardboard_req, 'paper': paper_req, 'lam': lam_req,
        'kol': kol, 'uppercost': uppercost,
        'lid_height': lid_height,
        'currency': cur_euro, 'feature': feature,
            }


def request_construction_cubbox(request):
    info = request_construction(request=request)
    return result_data_box(
        info["width"], info["length"], info["height"], info["cardboard"], info["paper"],
        info["kol"], info["lid_height"], info["currency"], info["lam"], info["uppercost"],
        info["feature"]
    )


def request_construction_cubboxinsert(request):
    info = request_construction(request=request)
    insert_height = int(request.POST['insert_height'].strip())
    return result_data_cdinsert(
        info["width"], info["length"], info["height"], insert_height,
        info["cardboard"], info["paper"],
        info["kol"], info["lid_height"], info["currency"], info["lam"], info["uppercost"],
        info["feature"]
    )


def request_construction_case(request):
    info = request_construction(request=request)
    return result_data_case(
        info["width"], info["length"], info["height"], info["cardboard"], info["paper"],
        info["kol"], info["currency"], info["lam"], info["uppercost"],
        info["feature"]
    )


def request_construction_casketm(request):
    info = request_construction(request=request)
    result = result_data_casket(
        info["width"], info["length"], info["height"], info["cardboard"], info["paper"],
        info["kol"], info["currency"], info["lam"], info["uppercost"],
        info["feature"]
    )
    return result


def request_construction_briefcase(request):
    info = request_construction(request=request)
    handle = request.POST['handle']
    return result_data_briefcase(
        info["width"], info["length"], info["height"], info["cardboard"], info["paper"],
        info["kol"], info["currency"], handle, info["lam"], info["uppercost"],
        info["feature"]
    )
