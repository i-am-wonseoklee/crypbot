"""Fetcher for simulation."""

import json
import logging
from typing import Dict, Optional

import requests

from crypbot.fetcher.base_fetcher import BaseFetcher


class SimulatedFetcher(BaseFetcher):
    """Fetcher providing past candle info (what user initialized)."""

    URL = "https://api.upbit.com/v1/candles/minutes/{period}"

    def __init__(self):
        self.__logger = logging.getLogger(__class__.__name__)
        self.__index = 0
        self.__data = json.dumps({})

    def initilaize(
        self, period: int, market: str, till: str, count: int, timeout: int = 5
    ) -> bool:
        """Initialize simulation fetcher.

        Args:
            period (int): Candle period in minutes.
            market (str): Market name (e.g. KRW-BTC).
            till (str): Time of the last candle in yyyy-MM-ddTHH:mm:ss:00+09:00 format.
            count (int): Number of candles.
            timeout (int): Timeout in seconds.

        Returns:
            bool: True if initialization succeeds, False otherwise.
        """
        try:
            response = requests.get(
                SimulatedFetcher.URL.format(period=period),
                params={"market": market, "to": till, "count": count},
                timeout=timeout,
            )
            response.raise_for_status()
            self.__index = 0
            self.__data = response.json()
            self.__data.reverse()
        except TimeoutError as err:
            self.__logger.error(err)
            return False
        except ValueError as err:
            self.__logger.error(err)
            return False
        except requests.exceptions.RequestException as err:
            self.__logger.error(err)
            return False
        return True

    def fetch_candle(self) -> Optional[Dict]:
        """Get a candle info.

        Returns:
            Optional[Dict]: Return a candle info. If there is nothing left, None.
        """
        now = self.__index
        if now >= len(self.__data):
            return None
        self.__index += 1
        return self.__create_candle(self.__data[now])

    def __create_candle(self, data: Dict) -> Dict:
        """Create candle data from a record of response.

        Args:
            data (Dict): A record of response.

        Returns:
            Dict: Candle data.
        """
        return {
            "market": data["market"],
            "date_time": data["candle_date_time_kst"],
            "opening_price": data["opening_price"],
            "high_price": data["high_price"],
            "low_price": data["low_price"],
            "closing_price": data["trade_price"],
            "acc_price": data["candle_acc_trade_price"],
            "acc_volume": data["candle_acc_trade_volume"],
        }

    @property
    def ncandles(self) -> int:
        """The number of remaining candles."""
        return len(self.__data) - self.__index
