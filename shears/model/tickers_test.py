"""Tests for tickers.py.
"""
import unittest

from collections import Counter

import tickers

class TestTicker(unittest.TestCase):
    """tickers tests.
    """

    def test_scrape_tickers_no_whitelist(self):
        text = "We love $GME and AMC, don't YOLO RKT! GME forever~"
        expected = Counter({
            'GME': 2,
            'AMC': 1,
            'YOLO': 1,  # Not a real mention, but expected without a whitelist.
            'RKT': 1,
        })
        self.assertEqual(tickers.scrape_tickers(text), expected)

    def test_scrape_tickers_with_whitelist(self):
        text = "We love $GME and AMC, don't YOLO RKT! GME forever~"
        expected = Counter({
            'GME': 2,
            'AMC': 1,
        })
        whitelist = frozenset(('GME', 'AMC'))
        self.assertEqual(
            tickers.scrape_tickers(text, whitelist=whitelist),
            expected)


if __name__ == '__main__':
    unittest.main()
