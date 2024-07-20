"""Buy and hold adviser test."""

import unittest

from crypbot.adviser import bnh_adviser
from crypbot.util import util


class BnhAdviserTest(unittest.TestCase):
    """Test buy and hold adviser."""

    def setUp(self):
        self.adviser = bnh_adviser.BnhAdviser(1000000.0, 10000.0, True, 2)

    def test_advise_order_no_candle(self):
        """Retun None if no candle data."""
        self.assertIsNone(self.adviser.advise_orders())

    def test_advise_orders_once(self):
        """Advise orders once."""
        self.adviser.update_candle(
            {
                "market": "KRW-BTC",
                "date_time": util.now(),
                "opening_price": 20000.0,
                "high_price": 20000.0,
                "low_price": 20000.0,
                "closing_price": 20000.0,
                "acc_price": 20000.0 * 20000,
                "acc_volume": 20000,
            }
        )
        orders0 = self.adviser.advise_orders()
        self.assertEqual(len(orders0), 1)
        self.assertEqual(orders0[0]["type"], "buy")
        self.assertEqual(orders0[0]["price"], 20000.0)
        self.assertEqual(orders0[0]["amount"], 25.0)
        self.assertEqual(self.adviser.balance, 1000000)

    def test_advise_orders_twice(self):
        """Advise orders twice."""
        self.adviser.update_candle(
            {
                "market": "KRW-BTC",
                "date_time": util.now(),
                "opening_price": 20000.0,
                "high_price": 20000.0,
                "low_price": 20000.0,
                "closing_price": 20000.0,
                "acc_price": 20000.0 * 20000,
                "acc_volume": 20000,
            }
        )
        for i in range(2):
            orders = self.adviser.advise_orders()
            self.assertEqual(len(orders), 1)
            self.assertEqual(orders[0]["type"], "buy")
            self.assertEqual(orders[0]["price"], 20000.0)
            self.assertEqual(orders[0]["amount"], 25.0)
            self.assertEqual(self.adviser.balance, 1000000.0 - i * 500000.0)
            self.adviser.update_order_result(
                {
                    "order": orders[0],
                    "exec_price": 20000.0,
                    "exec_amount": 25.0,
                    "fee": 0.0,
                    "state": "done",
                    "message": "",
                    "date_time": util.now(),
                }
            )
            self.assertEqual(self.adviser.balance, 1000000.0 - (i + 1) * 500000.0)
        self.assertIsNone(self.adviser.advise_orders())

    def test_advise_orders_twice_with_pending(self):
        """Advise orders twice with pending order."""
        self.adviser.update_candle(
            {
                "market": "KRW-BTC",
                "date_time": util.now(),
                "opening_price": 20000.0,
                "high_price": 20000.0,
                "low_price": 20000.0,
                "closing_price": 20000.0,
                "acc_price": 20000.0 * 20000,
                "acc_volume": 20000,
            }
        )
        orders0 = self.adviser.advise_orders()
        self.assertEqual(len(orders0), 1)
        self.assertEqual(orders0[0]["type"], "buy")
        self.assertEqual(orders0[0]["price"], 20000.0)
        self.assertEqual(orders0[0]["amount"], 25.0)
        self.assertEqual(self.adviser.balance, 1000000.0)
        self.adviser.update_order_result(
            {
                "order": orders0[0],
                "exec_price": 20000.0,
                "exec_amount": 25.0,
                "fee": 0.0,
                "state": "requested",
                "message": "",
                "date_time": util.now(),
            }
        )
        self.assertEqual(self.adviser.balance, 1000000.0)

        orders1 = self.adviser.advise_orders()
        self.assertEqual(len(orders1), 2)
        self.assertEqual(orders1[0]["type"], "cancel")
        self.assertEqual(self.adviser.balance, 1000000.0)
        self.adviser.update_order_result(
            {
                "order": orders1[1],
                "exec_price": 20000.0,
                "exec_amount": 25.0,
                "fee": 0.0,
                "state": "done",
                "message": "",
                "date_time": util.now(),
            }
        )
        self.assertEqual(self.adviser.balance, 500000.0)
