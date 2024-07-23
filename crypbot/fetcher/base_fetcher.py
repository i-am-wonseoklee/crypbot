"""Abstract class for fetcher that provides candle data."""

import abc
from typing import Dict, Optional


class BaseFetcher(metaclass=abc.ABCMeta):
    """Base class for fetcher."""

    @abc.abstractmethod
    def fetch_candle(self) -> Optional[Dict]:
        """Return a current candle as a dictionary.

        Returns:
            Dict: Candle information if exists. None otherwise.
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
