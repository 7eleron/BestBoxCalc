from PIL import Image, ImageDraw


def calc_xy(lis, lis_siz):
    im = Image.new('RGB', (lis_siz[0], lis_siz[1]), (192, 192, 192))
    draw = ImageDraw.Draw(im)
    for k in range(lis_siz[1] // lis[1]):
        start_y = lis[1] * k
        stop_y = lis[1] * (k + 1)
        for x in range(lis_siz[0] // lis[0]):
            start = lis[0] * x
            stop = lis[0] * (x + 1)
            draw.rectangle((start, start_y, stop, stop_y), fill='white', outline=(0, 0, 0))

    ost_0 = lis_siz[0] - ((lis_siz[0] // lis[0]) * lis[0])
    ost_1 = lis_siz[1] - ((lis_siz[1] // lis[1]) * lis[1])

    if ost_0 > lis[1]:
        start_x = lis_siz[0] - ost_0
        for x in range(1, (ost_0 // lis[1]) + 1):
            stop_x = start_x + lis[1]
            print(stop_x)
            start_y = 0
            for y in range(lis_siz[1] // lis[0]):
                stop_y = start_y + lis[0]
                draw.rectangle((start_x, start_y, stop_x, stop_y), fill='white', outline=(0, 0, 0))
                start_y = stop_y
            start_x = stop_x

    if ost_1 > lis[0]:
        start_y = lis_siz[1] - ost_1
        for k in range(1, (ost_1 // lis[0]) + 1):
            stop_y = start_y + lis[0]
            for x in range(lis_siz[0] // lis[1]):
                start = lis[1] * x
                stop = lis[1] * (x + 1)
                draw.rectangle((start, start_y, stop, stop_y), fill='white', outline=(0, 0, 0))
            start_y = stop_y

    im.save(f'details/views/calc_save/kroy_{lis[0]}x{lis[1]}.jpg', quality=95)
    return f'kroy_{lis[0]}x{lis[1]}'


def kroy(lis, var, lis_siz):
    if var == 0:
        name = calc_xy(lis, lis_siz)
    else:
        lis = [lis[1], lis[0]]
        name = calc_xy(lis, lis_siz)
    return name


