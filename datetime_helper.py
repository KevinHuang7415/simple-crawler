from datetime import date, timedelta

def fifteen_days_earlier(d):
    return date.today() - d >= timedelta(days=15)

def gen_date(ptt_date):
    date_arr = ptt_date.split('/')
    year = date.today().year
    month = date_arr[0]
    day = date_arr[1]
    try:
        return date(year, int(date_arr[0]), int(date_arr[1]))
    except ValueError:
        # no 2/29 this year, means the year must be earlier
        # set 1 year ago can fit current scenario
        if date_arr[0] == 2 and int(date_arr[1]) == 29:
            return date(year - 1, 2, 28)
        else:
            print('Error exists on date {y}/{m}/{d}'.format(y = year, m = month, d = day))
            return None

def earlier_date(date):
    date_diff = date - date.today()
    return date_diff <= timedelta(days=0)

def check_expired(ptt_date):
    d = gen_date(ptt_date)
    if not d:
        return True

    if (earlier_date(d)):
        return fifteen_days_earlier(d)
    else:
        try:
            d = d.replace(year = d.year - 1)
            return fifteen_days_earlier(d.replace(year = d.year - 1))
        # case for 2/29
        except ValueError:
            d = d + (date(d.year - 1, 3, 1) - date(d.year, 3, 1))
            return fifteen_days_earlier(d)
