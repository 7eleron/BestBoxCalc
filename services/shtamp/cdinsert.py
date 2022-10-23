def cutter(a, b, c):
    len_knif_tray = (c*4)+(a*4)+(b*4)
    total_len = len_knif_tray/100
    price = total_len*120
    return price


def resp_insert(a, b, tray_hight, lid_hight, insert_hight):
    lid = cutter(a, b, lid_hight)
    tray = cutter(a, b, tray_hight)
    insert = cutter(a, b, insert_hight)
    total_price = lid + tray + insert

    if total_price <= 2500:
        return 2500
    else:
        return total_price
