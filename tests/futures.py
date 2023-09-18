from qupyter.futures import get_ticker_list, get_trade_event
import unittest

class FuturesTests(unittest.TestCase):
    def test_get_ticker_list(self):
        tickers = get_ticker_list()
        self.assertEqual(tickers, ['10100', '10500'])

    def test_get_trade_event(self):
        df = get_trade_event('10100', '20230915')
        self.assertEqual(len(df), 114634)