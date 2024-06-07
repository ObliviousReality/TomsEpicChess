import math


def detect(xm, ym):
    if xm >= 30 and xm <= 30 + 80 * 8:
        xcell = math.ceil((xm - 30) / 80)
    else:
        xcell = 0
    if ym >= 30 and ym <= 30 + 80 * 8:
        ycell = math.ceil((ym - 30) / 80)
    else:
        ycell = 0
    return xcell, ycell
