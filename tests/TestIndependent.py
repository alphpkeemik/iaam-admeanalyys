from cmath import isnan
import unittest

from numpy import NaN
from components.independent import transform_age


class TestIndependent(unittest.TestCase):

    def test_transform_age(self):
        data = [
            (19, 'VA15', 1996, float("NaN"),  'only year'),
            (11.5, 'VA16', 2005, 6,  'year and month'),
            (NaN, float("NaN"), float("NaN"), 6, 'only month'),
        ]
        for expected, event, activesinceyear, activesincemonth, msg in data:
            actual = transform_age(
                event, activesinceyear,
                activesincemonth, float("NaN")
            )
            if isnan(expected):
                self.assertTrue(isnan(actual), msg)
            else:
                self.assertEqual(expected, actual, msg)
        data = [
            #            (NaN, 'random', float("NaN")),
            (4, '4 a', float("NaN")),
            (5, 'umbes 5 aastat', float("NaN")),
            (4.3, '4,3 a.', float("NaN")),
            (0.5, '6. kuud', float("NaN")),
            (4, 'random 2003 random 2005 random', 'LA07'),
            (10, 'random 1997 random 2005 aasta', 'LA07'),
        ]
        for expected, activesincetext, event in data:
            actual = transform_age(
                event, float("NaN"),
                float("NaN"), activesincetext
            )
            if isnan(expected):
                self.assertTrue(isnan(actual), activesincetext)
            else:
                self.assertEqual(expected, actual, activesincetext)


if __name__ == '__main__':
    unittest.main()
