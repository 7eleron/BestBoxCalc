def cutter(a, b, c):
    len_knif_lid_tray = ((a*2)+(b*2)) * 2
    len_knif_flap = ((a*2)+(c*2))*2
    total_len = (len_knif_lid_tray+len_knif_flap)/100
    price = total_len*120
    if a > 0 and a <= 100:
        price += 250 * 2
    elif a > 100 and a <= 350:
        price += 250 * 4
    elif a > 350:
        price += 250 * 6
    return price


def resp_folder(a, b, c):
    total_price = cutter(a, b, c)
    if total_price <= 2500:
        return 2500
    else:
        return total_price
