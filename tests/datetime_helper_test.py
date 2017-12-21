import unittest
from datetime import date, timedelta
import datetime_helper

class DatetimeHelperTestCase(unittest.TestCase):
    def setUp(self):
        self.year = date.today().year
        self.dates = {
            228: ('2/28', date(year=self.year, month=2, day=28)),
            229: ('2/29', date(year=self.year - 1, month=2, day=28)),
            230: ('2/30', None)
        }

    def test_gen_date(self):
        for d in self.dates.values():
            self.assertEqual(datetime_helper.gen_date(d[0]), d[1])

    def test_ptt_date_format(self):
        self.assertEqual(datetime_helper.ptt_date_format(date(year=self.year, month=2, day=28)), '2/28')
        self.assertEqual(datetime_helper.ptt_date_format(date(year=self.year, month=12, day=28)), '12/28')
        self.assertEqual(datetime_helper.ptt_date_format(date(year=self.year, month=2, day=8)), '2/08')

    def test_check_date_earlier(self):
        self.fail("Not implemented")

    def test_check_expired(self):
        today = date.today()
        term_dates = {
            0: [True, True, True, True],
            1: [True, True, True, True],
            5: [False, True, True, False],
            40: [False, True, True, False],
            -5: [True, True, True, True],
        }
        for term_date in term_dates:
            dates = [
                today - timedelta(days=2),
                today - timedelta(days=-2),
                today - timedelta(days=term_date + 2),
                today - timedelta(days=term_date - 2),
            ]
            test_cases = zip(dates, term_dates[term_date])
            for test_case in test_cases:
                d = datetime_helper.ptt_date_format(test_case[0])
                self.assertEqual(
                        datetime_helper.check_expired(d, term_date),
                        test_case[1],
                        'term date={0}, date={1}, today={2}'.format(term_date, test_case[0], today)
                )

if __name__ == '__main__':
    unittest.main()
