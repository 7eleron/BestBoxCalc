from details.algprog.calc_lis import calc
from details.algprog.round import rou


# картонная футляр
def case_cb(width, length, hight):
    indent = 5
    width_r = width+(hight*2)+indent
    length_r = (length*2)+hight+indent
    return [width_r, length_r]


# расход материала
def expence_case_cb(width, length, hight, lis_siz):
    case = case_cb(width, length, hight)
    case_exp = calc([case], lis_siz)[0]
    return {'Расход': rou(case_exp),
            'Информация': f'футляр {case[0]}x{case[1]}мм. '}
