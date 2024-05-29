import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from coinbaseloader import CoinbaseLoader, Granularity

class TestCoinbaseLoader(unittest.TestCase):

    @patch('coinbaseloader.CoinbaseLoader._get_req')
    def test_get_pairs(self, mock_get_req):
        mock_get_req.return_value = '[{"id": "btc-usdt", "base_currency": "BTC", "quote_currency": "USDT"}]'
        loader = CoinbaseLoader()
        pairs = loader.get_pairs()
        self.assertIsInstance(pairs, pd.DataFrame)
        self.assertFalse(pairs.empty)
        self.assertEqual(pairs.loc["btc-usdt", "base_currency"], "BTC")
        self.assertEqual(pairs.loc["btc-usdt", "quote_currency"], "USDT")

    @patch('coinbaseloader.CoinbaseLoader._get_req')
    def test_get_stats(self, mock_get_req):
        mock_get_req.return_value = '{"trade_id": 101718558, "price": "44609.81", "size": "0.001", "bid": "44609.81", "ask": "44609.82", "volume": "28632.46773751", "time": "2023-06-30T18:25:55.815404Z"}'
        loader = CoinbaseLoader()
        stats = loader.get_stats("btc-usdt")
        self.assertIsInstance(stats, pd.DataFrame)
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats.loc[0, "price"], "44609.81")

    @patch('coinbaseloader.CoinbaseLoader._get_req')
    def test_get_historical_data(self, mock_get_req):
        mock_get_req.return_value = '[["2023-06-30T00:00:00", "41650.0", "42600.0", "42310.8", "42368.21", "137.00913054"]]'
        loader = CoinbaseLoader()
        begin = datetime(2023, 1, 1)
        end = datetime(2023, 6, 30)
        granularity = Granularity.ONE_DAY
        data = loader.get_historical_data("btc-usdt", begin, end, granularity)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)
        self.assertEqual(data.index[0], pd.Timestamp("2023-06-30T00:00:00"))
        self.assertEqual(data.iloc[0]["open"], "42310.8")

if __name__ == '__main__':
    unittest.main()
