'''
Unit tests for datetime_helper module.
'''
import logging
import unittest
from datetime import date, timedelta
import datetime_helper

logging.disable(logging.CRITICAL)


class DatetimeHelperTestCase(unittest.TestCase):
    '''Test cases for datetime_helper.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.year = date.today().year
        cls.dates = {
            228: ('2/28', date(year=cls.year, month=2, day=28)),
            229: ('2/29', date(year=cls.year - 1, month=2, day=28)),
            230: ('2/30', None)
        }

        term_dates = {
            0: [True, True, True, True],
            1: [True, True, True, True],
            5: [False, True, True, False],
            40: [False, True, True, False],
            -5: [True, True, True, True],
        }

        cls.today = date.today()
        cls.test_cases = {}

        for term_date in term_dates:
            dates = [
                cls.today - timedelta(days=2),
                cls.today - timedelta(days=-2),
                cls.today - timedelta(days=term_date + 2),
                cls.today - timedelta(days=term_date - 2),
            ]
            cls.test_cases[term_date] = zip(dates, term_dates[term_date])

    def test_to_ptt_date_format(self):
        '''Unit test for datetime_helper.to_ptt_date_format.'''
        expect = date.today().strftime("%m/%d").lstrip('0')
        self.to_ptt_date_format(None, expect)

        year = self.year
        self.to_ptt_date_format(date(year=year, month=2, day=28), '2/28')
        self.to_ptt_date_format(date(year=year, month=12, day=28), '12/28')
        self.to_ptt_date_format(date(year=year, month=2, day=8), '2/08')

    def to_ptt_date_format(self, this_day, expect):
        '''A helper function for test_to_ptt_date_format.'''
        if this_day:
            ptt_date = datetime_helper.to_ptt_date_format(this_day)
        else:
            ptt_date = datetime_helper.to_ptt_date_format()

        self.assertEqual(ptt_date, expect)

    def test_check_expired(self):
        '''Unit test for pdatetime_helper.check_expired.'''
        for term_date, test_cases in self.test_cases.items():
            for test_case in test_cases:
                self.check_expired(test_case, term_date)

    def check_expired(self, test_case, term_date):
        '''A helper function for test_check_expired.'''
        ptt_date = datetime_helper.to_ptt_date_format(test_case[0])
        self.assertEqual(
            datetime_helper.check_expired(ptt_date, term_date),
            test_case[1],
            'term date={}, date={}, today={}'.format(
                term_date, test_case[0], self.today)
        )


if __name__ == '__main__':
    unittest.main()
