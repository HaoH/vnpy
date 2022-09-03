#!/usr/bin/env python
# coding: utf-8

# In[28]:


#%%
from datetime import datetime
from importlib import reload

import vnpy_portfoliostrategy
reload(vnpy_portfoliostrategy)

from vnpy_portfoliostrategy import BacktestingEngine
from vnpy.trader.constant import Interval
from vnpy.trader.optimize import OptimizationSetting

import vnpy_portfoliostrategy.strategies.pair_trading_strategy as stg
reload(stg)
from vnpy_portfoliostrategy.strategies.pair_trading_strategy import PairTradingStrategy


# In[29]:


#%%
engine = BacktestingEngine()
engine.set_parameters(
    vt_symbols=["y888.DCE", "p888.DCE"],
    interval=Interval.MINUTE,
    start=datetime(2019, 1, 1),
    end=datetime(2020, 4, 30),
    rates={
        "y888.DCE": 0/10000,
        "p888.DCE": 0/10000
    },
    slippages={
        "y888.DCE": 0,
        "p888.DCE": 0
    },
    sizes={
        "y888.DCE": 10,
        "p888.DCE": 10
    },
    priceticks={
        "y888.DCE": 1,
        "p888.DCE": 1
    },
    capital=1_000_000,
)

setting = {
    "boll_window": 20,
    "boll_dev": 1,
}
engine.add_strategy(PairTradingStrategy, setting)


# In[ ]:


#%%
engine.load_data()
engine.run_backtesting()
df = engine.calculate_result()
engine.calculate_statistics()
engine.show_chart()


# In[ ]:


setting = OptimizationSetting()
setting.set_target("sharpe_ratio")
setting.add_parameter("boll_window", 10, 30, 1)
setting.add_parameter("boll_dev", 1, 3, 1)

engine.run_ga_optimization(setting)


# In[ ]:


engine.run_bf_optimization(setting)

