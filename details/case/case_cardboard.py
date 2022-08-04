from details.algprog.calc_lis import calc


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
    return {'Расход': float(case_exp),
            'Информация': f'{case[0]}x{case[1]}мм. '}
