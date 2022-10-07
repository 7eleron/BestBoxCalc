from cubbox.result import result_data_box
from casketM.result import result_data_casket
from casketMbriefcase.result import result_data_briefcase
from Case.result import result_data_case
from CubBoxInsert.result import result_data_cdinsert


def request_construction_cubbox(request):
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
        request.POST['hight'].strip())
    kol = int(request.POST['kol'].strip())
    lid_hight = int(request.POST['lid_hight'].strip())
    uppercost = float(request.POST['uppercost'].strip())
    result = result_data_box(a, b, c, cardboard_req, paper_req, kol, lid_hight, cur_euro, lam_req, uppercost)
    return result


def request_construction_cubboxinsert(request):
    req_cur_euro = request.POST['currency'].strip().split(',')
    cur_euro = 0
    if len(req_cur_euro) == 1:
        cur_euro = float(req_cur_euro[0])
    elif len(req_cur_euro) == 2:
        cur_euro = float(req_cur_euro[0] + '.' + req_cur_euro[1])
    cardboard_req = request.POST['cardboard']
    paper_req = request.POST['paper']
    lam_req_lid = request.POST['laminatinglid']
    lam_req_insert = request.POST['laminatinginsert']
    lam_req = [lam_req_lid, lam_req_insert]
    a, b, c = int(request.POST['width'].strip()), int(request.POST['length'].strip()), int(
        request.POST['hight'].strip())
    kol = int(request.POST['kol'].strip())
    lid_hight = int(request.POST['lid_hight'].strip())
    insert_hight = int(request.POST['insert_hight'].strip())
    uppercost = float(request.POST['uppercost'].strip())
    result = result_data_cdinsert(a, b, c, insert_hight, cardboard_req, paper_req, kol, lid_hight, cur_euro, lam_req,
                                  uppercost)
    return result


def request_construction_case(request):
    req_cur_euro = request.POST['currency'].strip().split(',')
    cur_euro = 0
    if len(req_cur_euro) == 1:
        cur_euro = float(req_cur_euro[0])
    elif len(req_cur_euro) == 2:
        cur_euro = float(req_cur_euro[0] + '.' + req_cur_euro[1])
    cardboard_req = request.POST['cardboard']
    paper_req = request.POST['paper']
    lam_req_case = request.POST['laminatinglid']
    lam_req_tray = request.POST['laminatingtray']
    lam_req = [lam_req_case, lam_req_tray]
    a, b, c = int(request.POST['width'].strip()), int(request.POST['length'].strip()), int(
        request.POST['hight'].strip())
    kol = int(request.POST['kol'].strip())
    uppercost = float(request.POST['uppercost'].strip())
    result = result_data_case(a, b, c, cardboard_req, paper_req, kol, cur_euro, lam_req, uppercost)
    return result


def request_construction_casketm(request):
    req_cur_euro = request.POST['currency'].strip().split(',')
    cur_euro = 0
    if len(req_cur_euro) == 1:
        cur_euro = float(req_cur_euro[0])
    elif len(req_cur_euro) == 2:
        cur_euro = float(req_cur_euro[0] + '.' + req_cur_euro[1])
    cardboard_req = request.POST['cardboard']
    paper_req = request.POST['paper']
    lam_req_lid = 'без кашировки'
    lam_req_tray = request.POST['laminatingtray']
    lam_req = [lam_req_lid, lam_req_tray]
    a, b, c = int(request.POST['width'].strip()), int(request.POST['length'].strip()), int(
        request.POST['hight'].strip())
    kol = int(request.POST['kol'].strip())
    uppercost = float(request.POST['uppercost'].strip())
    result = result_data_casket(a, b, c, cardboard_req, paper_req, kol, cur_euro, lam_req, uppercost)
    return result


def request_construction_briefcase(request):
    req_cur_euro = request.POST['currency'].strip().split(',')
    cur_euro = 0
    if len(req_cur_euro) == 1:
        cur_euro = float(req_cur_euro[0])
    elif len(req_cur_euro) == 2:
        cur_euro = float(req_cur_euro[0] + '.' + req_cur_euro[1])
    handle = request.POST['handle']
    cardboard_req = request.POST['cardboard']
    paper_req = request.POST['paper']
    lam_req_lid = 'без кашировки'
    lam_req_tray = request.POST['laminatingtray']
    lam_req = [lam_req_lid, lam_req_tray]
    a, b, c = int(request.POST['width'].strip()), int(request.POST['length'].strip()), int(
        request.POST['hight'].strip())
    kol = int(request.POST['kol'].strip())
    uppercost = float(request.POST['uppercost'].strip())
    result = result_data_briefcase(a, b, c, cardboard_req, paper_req, kol, cur_euro, handle, lam_req, uppercost)
    return result
