from abc import ABC
from types import ModuleType
from typing import Optional, List, Callable, Dict
from importlib import import_module

from .constant import Market
from .object import HistoryRequest, TickData, BarData
from .setting import SETTINGS


class BaseDatafeed(ABC):
    """
    Abstract datafeed class for connecting to different datafeed.
    """

    def init(self, output: Callable = print) -> bool:
        """
        Initialize datafeed service connection.
        """
        pass

    def query_bar_history(self, req: HistoryRequest, output: Callable = print) -> Optional[List[BarData]]:
        """
        Query history bar data.
        """
        output("查询K线数据失败：没有正确配置数据服务")

    def query_index_bar_history(self, req: HistoryRequest, output: Callable = print) -> Optional[List[BarData]]:
        """
        Query history bar data.
        """
        pass

    def query_tick_history(self, req: HistoryRequest, output: Callable = print) -> Optional[List[TickData]]:
        """
        Query history tick data.
        """
        output("查询Tick数据失败：没有正确配置数据服务")

    def handle_bar_data(self, df, symbol, exchange, interval, start, end):
        """
        convert df to List[BarData]

        """
        return []

    def index_components(self, symbol, output: Callable = print):
        """
        Query index components
        """
        output("查询指数成分股失败：没有正确配置数据服务")

    def get_ex_factor(self, symbols, output: Callable = print):
        """
        Query ex_factor
        """
        output("查询复权因子失败：没有正确配置数据服务")

    def get_shares(self, symbols, start_date, end_date, output: Callable = print):
        """
        Query shares
        """
        output("查询股本信息失败：没有正确配置数据服务")


datafeed: BaseDatafeed = None


def get_datafeed() -> BaseDatafeed:
    """"""
    # Return datafeed object if already inited
    global datafeed
    if datafeed:
        return datafeed

    # Read datafeed related global setting
    datafeed_name: str = SETTINGS["datafeed.name"]

    if not datafeed_name:
        datafeed = BaseDatafeed()

        print("没有配置要使用的数据服务，请修改全局配置中的datafeed相关内容")
    else:
        module_name: str = f"vnpy_{datafeed_name}"

        # Try to import datafeed module
        try:
            module: ModuleType = import_module(module_name)

            # Create datafeed object from module
            datafeed = module.Datafeed()
        # Use base class if failed
        except ModuleNotFoundError:
            datafeed = BaseDatafeed()

            print(f"无法加载数据服务模块，请运行 pip install {module_name} 尝试安装")

    return datafeed


datafeeds: Dict[Market, BaseDatafeed] = {}


def get_datafeeds() -> Dict[Market, BaseDatafeed]:
    """
    不同的市场使用不同的datafeed
    """
    global datafeeds
    if datafeeds and len(datafeeds) > 0:
        return datafeeds

    # Read datafeed related global setting
    datafeed_type = SETTINGS["datafeed.type"]
    if datafeed_type == "single":
        datafeed = get_datafeed()
        for m in Market:
            datafeeds[m] = datafeed
    elif datafeed_type == "mix":
        for m in Market:
            mv = m.value.lower()
            datafeed_name: str = SETTINGS["datafeed.name.{}".format(mv)]
            module_name: str = f"vnpy_{datafeed_name}"

            # Try to import datafeed module
            try:
                module: ModuleType = import_module(module_name)
            except ModuleNotFoundError:
                print(f"找不到数据服务驱动{module_name}，使用默认的RQData数据服务")
                module: ModuleType = import_module("vnpy_rqdata")

            # Create datafeed object from module
            username: str = SETTINGS["datafeed.username.{}".format(datafeed_name)]
            password: str = SETTINGS["datafeed.password.{}".format(datafeed_name)]
            dataf = module.Datafeed(username, password)

            datafeeds[m] = dataf

    return datafeeds
