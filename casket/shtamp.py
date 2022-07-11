
def cutter_tray(a, b, c):
    len_knif_tray = (c*4)+(a*4)+(b*4)
    total_len = len_knif_tray/100
    price = total_len*146.5
    return price


def cutter_folder(a, b, c):
    len_knif_lid_tray = (a*2)+(b*2)
    len_knif_flap = ((a*2)+(c*2))*2
    total_len = (len_knif_lid_tray+len_knif_flap)/100
    price = total_len*146.5
    return price


def resp(a, b, c):
    if a <= 100:
        punch = 300*2
    elif a <= 300 and a >= 110:
        punch = 300*4
    else:
        punch = 300 * 6
    total_price = cutter_folder(a, b, c) + cutter_tray(a, b, c) + punch
    if total_price <= 2500:
        return 2500
    else:
        return total_price
