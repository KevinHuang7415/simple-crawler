from datetime import date, timedelta

def expired(d, term_date):
    return date.today() - d >= timedelta(days = term_date)

def gen_date(ptt_date):
    date_arr = ptt_date.split('/')
    year = date.today().year
    month = int(date_arr[0])
    day = int(date_arr[1])
    try:
        return date(year, month, day)
    except ValueError:
        # no 2/29 this year, means the year must be earlier
        # set 2/28 to last year can fit current scenario
        if month == 2 and day == 29:
            return date(year - 1, 2, 28)
        else:
            print('Error exists on date {y}/{m}/{d}'.format(y = year, m = month, d = day))
            return None

def earlier_date(date):
    date_diff = date - date.today()
    return date_diff <= timedelta(days=0)

def check_expired(ptt_date, term_date = 15):
    d = gen_date(ptt_date)
    if not d:
        return True

    if (earlier_date(d)):
        return expired(d, term_date)
    else:
        try:
            d = d.replace(year = d.year - 1)
            return expired(d, term_date)
        # case for 2/29
        except ValueError:
            d = d + (date(d.year - 1, 3, 1) - date(d.year, 3, 1))
            return expired(d, term_date)
