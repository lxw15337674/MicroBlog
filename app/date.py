import time, datetime


def date():
    t1 = time.strftime("%Y-%m-%d %X", time.localtime())
    t = time.strptime(t1, "%Y-%m-%d %X")
    y, m, d, h, m1, s = t[0:6]
    date = datetime.datetime(y, m, d, h, m1, s)
    return date
