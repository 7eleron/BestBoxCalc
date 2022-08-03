def cutter(a, b, c):
    len_knif = (a*4)+(c*6)+(b*6)
    total_len = len_knif/100
    price = total_len*146.5
    return price


def resp_case(a, b, c):
    total_price = cutter(a, b, c)
    if total_price <= 2500:
        return 2500
    else:
        return total_price