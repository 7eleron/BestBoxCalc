def cutter_folder(a, b, c):
    len_knif_lid_tray = (a*2)+(b*2)
    len_knif_flap = ((a*2)+(c*2))*2
    total_len = (len_knif_lid_tray+len_knif_flap)/100
    price = total_len*146.5
    return price


def resp(a, b, c):
    total_price = cutter_folder(a, b, c)
    if total_price <= 2500:
        return 2500
    else:
        return total_price
