"""Abstract class for adviser that decides whether to buy."""

import abc
from typing import Dict, List, Optional


class BaseAdviser(metaclass=abc.ABCMeta):
    """Base class for adviser."""

    def __init__(self, budget: int, min_price: int, use_simtime: bool = False):
        """C'tor.

        Args:
            budget (int): Total budget.
            min_price (int): Minimum order price.
            use_simtime (bool): True when simulation, False otherwise.
        """
        self._balance = budget
        self.__budget = budget
        self.__min_price = min_price
        self.__use_simtime = use_simtime

    @property
    def balance(self) -> int:
        """Current balance."""
        return self._balance

    @property
    def budget(self) -> int:
        """Total budget."""
        return self.__budget

    @property
    def min_price(self) -> int:
        """Minimum order price."""
        return self.__min_price

    @property
    def use_simtime(self) -> bool:
        """Boolean whether to use simulation time."""
        return self.__use_simtime

    @abc.abstractmethod
    def advise_orders(self) -> Optional[List[Dict]]:
        """Advise trading orders.

        Returns:
            Optional[List[Dict]]: Trading orders. None for hold.
            [{
                "id"        : Request id such as "1721492171.951993" (epoch, str).
                "type"      : One of ["sell", "buy", "cancel"].
                "price"     : Order price.
                "amount"    : Order amount.
                "date_time" : Timestamp of this advice.
            }]
        """

    @abc.abstractmethod
    def update_candle(self, candle: Dict):
        """Update a candle info.

        Args:
            candle (Dict): A candle from fetcher.
            {
                "market"        : str
                "date_time"     : str
                "opening_price" : float
                "high_price"    : float
                "low_price"     : float
                "closing_price" : float
                "acc_price"     : float
                "acc_volume"    : float
            }
        """

    @abc.abstractmethod
    def update_order_result(self, result: Dict):
        """Update an order result.

        Args:
            result (Dict): Order result.
            {
                "order"         : An order made by `advise_order` (Dict).
                "exec_price"    : Executed price.
                "exec_amount    : Executed amount.
                "fee"           : Fee.
                "state"         : One of ["requested", "done"].
                "message"       : Result message if exists. None if not.
                "date_time"     : Timestamp of the result.
            }
        """
