"""Buy and hold adviser."""

import copy
import logging

from typing import Dict, List, Optional

from crypbot.adviser.base_adviser import BaseAdviser
from crypbot.util import util


class BnhAdviser(BaseAdviser):
    """_summary_."""

    def __init__(
        self, budget: int, min_price: int, use_simtime: bool = False, nbuys: int = 3
    ):
        """C'tor.

        Args:
            budget (int): Total budget.
            min_price (int): Minimum order price.
            use_simtime (bool): True when simulation, False otherwise.
            nbuys (int): The number of buys before hold.
        """
        super().__init__(budget, min_price, use_simtime)
        self.__logger = logging.getLogger(__class__.__name__)
        self.__nbuys = nbuys
        self.__candles = []
        self.__waiting_orders = {}

    def advise_orders(self) -> Optional[List[Dict]]:
        """Advise orders.

        Returns:
            Optional[List[Dict]]: Trading orders. None for hold.
        """
        if len(self.__candles) == 0:
            self.__logger.error("No candle info.")
            return None

        cprice = self.__candles[-1]["closing_price"]

        target = self.budget / self.__nbuys
        if target > self.balance:
            target = self.balance

        amount = round(target / cprice, 4)
        target = round(amount * cprice)

        if target < self.min_price or target > self.balance:
            return None

        now = self.__candles[-1]["date_time"] if self.use_simtime else util.now()

        orders = []
        for order in self.__waiting_orders.values():
            orders.append(
                {
                    "id": order["id"],
                    "type": "cancel",
                    "price": 0,
                    "amount": 0,
                    "date_time": now,
                }
            )
        orders.append(
            {
                "id": util.now("epoch"),
                "type": "buy",
                "price": cprice,
                "amount": amount,
                "date_time": now,
            }
        )

        return orders

    def update_candle(self, candle: Dict):
        """Append a candle info.

        Args:
            candle (Dict): Candle info from fetcher.
        """
        self.__candles.append(copy.deepcopy(candle))

    def update_order_result(self, result: Dict):
        """Update an order result.

        Args:
            result (Dict): Order result.
        """
        if result["state"] == "requested":
            self.__waiting_orders[result["order"]["id"]] = result["order"]
        else:
            if result["order"]["id"] in self.__waiting_orders:
                del self.__waiting_orders[result["order"]["id"]]

            total = float(result["exec_price"]) * float(result["exec_amount"])
            if result["order"]["type"] == "buy":
                self._balance -= total + result["fee"]
            elif result["order"]["type"] == "sell":
                self._balance += total - result["fee"]
