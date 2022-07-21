def cutter_tray(a, b, c):
    len_knif_tray = (c*4)+(a*4)+(b*4)
    total_len = len_knif_tray/100
    price = total_len*146.5
    return price


def resp(a, b, c):
    total_price = cutter_tray(a, b, c)
    if total_price <= 2500:
        return 2500
    else:
        return total_price
