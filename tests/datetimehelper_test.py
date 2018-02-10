'''
Unit tests for datetimehelper module.
'''
import logging
import unittest
from datetime import date, timedelta, datetime, time
import datetimehelper as dh

logging.disable(logging.CRITICAL)


class DatetimeHelperTestCase(unittest.TestCase):
    '''Test cases for datetimehelper.'''

    @classmethod
    def setUpClass(cls):
        '''The class level setup.'''
        cls.today = date.today()

    def test_to_ptt_date(self):
        '''Unit test for datetimehelper.to_ptt_date.'''
        expect = date.today().strftime("%m/%d").lstrip('0')
        self.to_ptt_date(None, expect)

        year = date.today().year
        self.to_ptt_date(date(year=year, month=2, day=28), '2/28')
        self.to_ptt_date(date(year=year, month=12, day=28), '12/28')
        self.to_ptt_date(date(year=year, month=2, day=8), '2/08')

    def to_ptt_date(self, this_day, expect):
        '''A helper function for test_to_ptt_date.'''
        if this_day:
            ptt_date = dh.to_ptt_date(this_day)
        else:
            ptt_date = dh.to_ptt_date()

        self.assertEqual(ptt_date, expect)

    def test_check_expired(self):
        '''Unit test for datetimehelper.check_expired.'''
        test_case_list = {}

        # see the detail for date_list
        term_date_expect_list = {
            0: [True, True, True, True],
            1: [True, True, True, True],
            5: [False, True, True, False],
            40: [False, True, True, False],
            -5: [True, True, True, True],
        }

        for term_date in term_date_expect_list:
            date_list = [
                # 2 days before today
                self.today - timedelta(days=2),
                # 2 days after today
                self.today - timedelta(days=-2),
                # 2 days earlier than term date
                self.today - timedelta(days=term_date + 2),
                # 2 days later than term date
                self.today - timedelta(days=term_date - 2),
            ]
            test_case_list[term_date] =\
                zip(date_list, term_date_expect_list[term_date])

        for term_date, test_cases in test_case_list.items():
            for test_case in test_cases:
                self.check_expired(test_case, term_date)

    def check_expired(self, test_case, term_date):
        '''A helper function for test_check_expired.'''
        ptt_date = dh.to_ptt_date(test_case[0])
        self.assertEqual(
            dh.check_expired(ptt_date, term_date),
            test_case[1],
            'term date={}, date={}, today={}'.format(
                term_date, test_case[0], self.today)
        )

    def test_alt_to_full(self):
        '''Unit test for datetimehelper.alt_to_full.'''
        datetime_str = '12/26/2017 15:56:57'
        expect = 'Tue Dec 26 15:56:57 2017'
        self.assertEqual(dh.alt_to_full(datetime_str), expect)

    def test_to_full_datetime(self):
        '''Unit test for datetimehelper.to_full_datetime.'''
        ptt_date = '12/26'
        full_date = dh.to_full_datetime(ptt_date)

        datetime_obj = datetime.strptime(full_date, dh._FORMAT_FULL)
        self.assertEqual(datetime_obj.month, 12)
        self.assertEqual(datetime_obj.day, 26)
        self.assertEqual(datetime_obj.time(), time(hour=12))

        ptt_date = '2/30'
        self.assertIsNone(dh.to_full_datetime(ptt_date))

    def test_to_datetime(self):
        '''Unit test for datetimehelper.to_datetime.'''
        datetime_obj = dh.to_datetime('Tue Dec 26 15:56:57 2017')
        self.assertEqual(datetime_obj.year, 2017)
        self.assertEqual(datetime_obj.month, 12)
        self.assertEqual(datetime_obj.day, 26)
        self.assertEqual(datetime_obj.hour, 15)


if __name__ == '__main__':
    unittest.main()
