'''
Helper functions for date-time.
'''
from datetime import date, timedelta
import logging

LOGGER = logging.getLogger('.'.join(['crawler', __name__]))


def to_ptt_date_format(date_obj=date.today()):
    '''Date time object to PTT format string.'''
    return date_obj.strftime("%m/%d").lstrip('0')


def _gen_date(ptt_date):
    '''Generate date object for date in PTT format.'''
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
        LOGGER.error('Error exists on date [%d/%d/%d]', year, month, day)
        return None


def _check_date_earlier(this_day, days):
    '''Check if the day is days earlier than today.'''
    date_diff = date.today() - this_day
    return date_diff >= timedelta(days=days), date_diff.days


def check_expired(ptt_date, term_date=15):
    '''Check if the date in PTT format expired.'''
    if term_date < 0:
        LOGGER.warning(
            'Given term date being later than today is illegal: [%d]',
            term_date
        )
        return True

    LOGGER.debug('Input date: [%s]', ptt_date)
    date_obj = _gen_date(ptt_date)
    if not date_obj:
        return True

    earlier, days_diff = _check_date_earlier(date_obj, 0)
    if earlier:
        return days_diff >= term_date
    else:
        # no article date can be later in reality
        # set year to last year can fit current scenario
        try:
            date_obj = date_obj.replace(year=date_obj.year - 1)
            return _check_date_earlier(date_obj, term_date)[0]
        # case for 2/29
        except ValueError:
            date_obj = date_obj + (date(date_obj.year - 1, 3, 1) - date(date_obj.year, 3, 1))
            return _check_date_earlier(date_obj, term_date)[0]
