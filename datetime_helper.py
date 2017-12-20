from datetime import date, timedelta

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

def check_date_earlier(d, term_date):
    date_diff = date.today() - d
    return date_diff >= timedelta(days = term_date), date_diff.days

def check_expired(ptt_date, term_date = 15):
    d = gen_date(ptt_date)
    if not d:
        return True

    earlier, days_diff = check_date_earlier(d, 0)
    if earlier:
        return days_diff >= term_date
    else:
        # no article date can be later in reality
        # set year to last year can fit current scenario
        try:
            d = d.replace(year=d.year - 1)
            return check_date_earlier(d, term_date)[0]
        # case for 2/29
        except ValueError:
            d = d + (date(d.year - 1, 3, 1) - date(d.year, 3, 1))
            return check_date_earlier(d, term_date)[0]
