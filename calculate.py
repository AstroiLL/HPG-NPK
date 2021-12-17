def isnoneto0(x):
    return 0 if x is None else x


def calc(n, nh4=None, no3=None, nh4no3=None):
    if nh4no3 is None and nh4 is None:
        nh4no3 = 1 - (no3 / n)
        nh4 = n * nh4no3
        return nh4no3, nh4
    elif nh4no3 is None and no3 is None:
        nh4no3 = nh4 / n
        no3 = n * (1 - nh4no3)
        return nh4no3, no3
    elif no3 is None and nh4 is None:
        no3 = n * (1 - nh4no3)
        nh4 = n * nh4no3
        return no3, nh4
    else:
        return None, None
