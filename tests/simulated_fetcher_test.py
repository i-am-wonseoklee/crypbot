"""Simulated fetcher test."""

import unittest

from crypbot.fetcher import simulated_fetcher


class SimulatedFetcherTest(unittest.TestCase):
    """Test SimulatedFetcher."""

    def setUp(self):
        self.fetcher = simulated_fetcher.SimulatedFetcher()
        self.assertTrue(
            self.fetcher.initilaize(
                period=1, market="KRW-BTC", till="2024-07-17T00:00", count=10
            )
        )

    def test_initialize(self):
        """Test `initilaize`."""
        self.assertEqual(self.fetcher.ncandles, 10)

    def test_fetch_candle(self):
        """Test `fetch_candle`."""
        candle = self.fetcher.fetch_candle()
        self.assertEqual(candle["market"], "KRW-BTC")
