#!/usr/bin/env python
# coding: utf-8

# In[1]:


#%%
from vnpy.trader.optimize import OptimizationSetting
from vnpy_spreadtrading.backtesting import BacktestingEngine
from vnpy_spreadtrading.strategies.statistical_arbitrage_strategy import (
    StatisticalArbitrageStrategy
)
from vnpy_spreadtrading.base import LegData, SpreadData
from datetime import datetime


# In[2]:


spread = SpreadData(
    name="IF-Spread",
    legs=[LegData("IF1911.CFFEX"), LegData("IF1912.CFFEX")],
    variable_symbols={"A": "IF1911.CFFEX", "B": "IF1912.CFFEX"},
    variable_directions={"A": 1, "B": -1},
    price_formula="A-B",
    trading_multipliers={"IF1911.CFFEX": 1, "IF1912.CFFEX": 1},
    active_symbol="IF1911.CFFEX",
    min_volume=1,
    compile_formula=False                          # 回测时不编译公式，compile_formula传False，从而支持多进程优化
)


# In[3]:


#%%
engine = BacktestingEngine()
engine.set_parameters(
    spread=spread,
    interval="1m",
    start=datetime(2019, 6, 10),
    end=datetime(2019, 11, 10),
    rate=0,
    slippage=0,
    size=300,
    pricetick=0.2,
    capital=1_000_000,
)
engine.add_strategy(StatisticalArbitrageStrategy, {})


# In[ ]:


#%%
engine.load_data()
engine.run_backtesting()
df = engine.calculate_result()
engine.calculate_statistics()
engine.show_chart()


# In[ ]:


for trade in engine.trades.values():
    print(trade)


# In[ ]:


setting = OptimizationSetting()
setting.set_target("sharpe_ratio")
setting.add_parameter("boll_window", 10, 30, 1)
setting.add_parameter("boll_dev", 1, 3, 1)

engine.run_ga_optimization(setting)


# In[ ]:


engine.run_bf_optimization(setting)

