def cutter(a, b, c, hight_lid):
    len_knif_lid = (hight_lid*4)+((a+5)*4)+((b+5)*4)
    len_knif_tray = (c*4)+(a*4)+(b*4)
    total_len = (len_knif_tray+len_knif_lid)/100
    test_price = total_len*130
    if test_price <= 2500:
        return 2500
    else:
        return test_price
