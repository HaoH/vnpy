from abc import ABC, abstractmethod
from datetime import datetime
from types import ModuleType
from typing import List, Dict, Union
from dataclasses import dataclass
from importlib import import_module

from .constant import Interval, Exchange, Market, Conflict
from .object import BarData, TickData, BaseData
from .setting import SETTINGS
from .utility import ZoneInfo

from ex_vnpy.object import BasicStockData, BasicIndexData, BasicSymbolData, ExBarData, SharesData, DailyStatData

DB_TZ = ZoneInfo(SETTINGS["database.timezone"])


def convert_tz(dt: datetime) -> datetime:
    """
    Convert timezone of datetime object to DB_TZ.
    """
    dt: datetime = dt.astimezone(DB_TZ)
    return dt.replace(tzinfo=None)


@dataclass
class BarOverview(BaseData):
    """
    Overview of bar data stored in database.
    """

    symbol: str = ""
    symbol_id: int = 0
    exchange: Exchange = None
    interval: Interval = None
    count: int = 0
    start: datetime = None
    end: datetime = None
    stype: str = "CS"


@dataclass
class TickOverview(BaseData):
    """
    Overview of tick data stored in database.
    """

    symbol: str = ""
    exchange: Exchange = None
    count: int = 0
    start: datetime = None
    end: datetime = None


class BaseDatabase(ABC):
    """
    Abstract database class for connecting to different database.
    """

    @abstractmethod
    def save_bar_data(self, bars: List[BarData], stream: bool = False, conflict: Conflict = Conflict.REPLACE) -> bool:
        """
        Save bar data into database.
        """
        pass

    @abstractmethod
    def save_tick_data(self, ticks: List[TickData], stream: bool = False,
                       conflict: Conflict = Conflict.REPLACE) -> bool:
        """
        Save tick data into database.
        """
        pass

    @abstractmethod
    def load_bar_data(
            self,
            symbol: str,
            exchange: Exchange,
            interval: Interval,
            start: datetime,
            end: datetime,
            stype: str = None
    ) -> List[BarData]:
        """
        Load bar data from database.
        """
        pass

    @abstractmethod
    def load_ex_bar_data(
            self,
            symbol: str,
            exchange: Exchange,
            interval: Interval,
            start: datetime,
            end: datetime,
            stype: str = None
    ) -> List[ExBarData]:
        pass

    @abstractmethod
    def load_daily_stat_data(
            self,
            interval: Interval,
            start: datetime,
            end: datetime,
            symbol: str = None,
            exchange: Exchange = None,
            stype: str = "CS"
    ) -> List[DailyStatData]:
        pass

    @abstractmethod
    def load_tick_data(
            self,
            symbol: str,
            exchange: Exchange,
            start: datetime,
            end: datetime
    ) -> List[TickData]:
        """
        Load tick data from database.
        """
        pass

    @abstractmethod
    def delete_bar_data(
            self,
            symbol: str,
            exchange: Exchange,
            interval: Interval
    ) -> int:
        """
        Delete all bar data with given symbol + exchange + interval.
        """
        pass

    @abstractmethod
    def delete_tick_data(
            self,
            symbol: str,
            exchange: Exchange
    ) -> int:
        """
        Delete all tick data with given symbol + exchange.
        """
        pass

    @abstractmethod
    def get_bar_overview(self, symbol_id: int = None, symbol: str = None, stype: str = "CS") -> List[BarOverview]:
        """
        Return bar data avaible in database.
        """
        pass

    @abstractmethod
    def get_tick_overview(self) -> List[TickOverview]:
        """
        Return tick data avaible in database.
        """
        pass

    @abstractmethod
    def get_symbol_ids_by_market(self, s_type: str, market: Market) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_symbol_ids_by_symbols(self, vt_symbols: list) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_basic_stock_data(self, markets: List[Market]) -> [Market, List[BasicStockData]]:
        """
        Return data available in database.
        """
        pass

    @abstractmethod
    def get_basic_index_data(self, markets: List[Market]) -> Dict[Market, List[BasicIndexData]]:
        pass

    @abstractmethod
    def get_basic_info_by_symbols(self, symbols, market: Market = Market.CN, symbol_type: str = 'CS') -> List[BasicSymbolData]:
        pass

    @abstractmethod
    def update_daily_stat_data(self, many_data: List, conflict: Conflict = Conflict.IGNORE, new_inds: List[str] = None):
        pass

    @abstractmethod
    def save_operation_log(self, type: str, op_status: str, op_time: datetime, op_info: str = ""):
        pass

    @abstractmethod
    def save_capital_data(self, capital_data: List):
        pass

    @abstractmethod
    def save_capital_flat_data(self, capital_data: List):
        pass

    def update_stocks_meta_data(self, stocks_data):
        pass

    def get_capital_days(self, month_first_day, month_last_day) -> List[str]:
        pass

    def get_auction_days(self, month_first_day, month_last_day) -> List[str]:
        pass

    def get_latest_statistic_date(self):
        pass

    def get_latest_op_info(self, op_type):
        pass

    def update_aliyun_binlog_files(self, binlog_files: List):
        pass

    def get_new_binlog_files(self) -> List:
        pass

    def get_capital_data_by_month(self, month) -> List:
        pass

    def get_capital_flat_data_by_symbol(self, symbol_id, start_dt: datetime = None, end_dt: datetime = None) -> List:
        pass

    def get_latest_overview_date(self, market: Market):
        pass

    def save_shares_data(self, bars: List[SharesData], change_starts: List = None, stream: bool = False, conflict: Conflict = Conflict.REPLACE) -> bool:
        """
        Save shares data into database.
        """
        pass

database: BaseDatabase = None


def get_database() -> BaseDatabase:
    """"""
    # Return database object if already inited
    global database
    if database:
        return database

    # Read database related global setting
    database_name: str = SETTINGS["database.name"]
    module_name: str = f"vnpy_{database_name}"

    # Try to import database module
    try:
        module: ModuleType = import_module(module_name)
    except ModuleNotFoundError:
        print(f"找不到数据库驱动{module_name}，使用默认的SQLite数据库")
        module: ModuleType = import_module("vnpy_sqlite")

    # Create database object from module
    database = module.Database()
    return database
