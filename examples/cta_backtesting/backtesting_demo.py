#!/usr/bin/env python
# coding: utf-8

# In[1]:


#%%
from vnpy.trader.optimize import OptimizationSetting
from vnpy_ctastrategy.backtesting import BacktestingEngine
from vnpy_ctastrategy.strategies.atr_rsi_strategy import (
    AtrRsiStrategy,
)
from vnpy_ctastrategy.strategies.boll_channel_strategy import BollChannelStrategy
from vnpy_ctastrategy.strategies.double_ma_strategy import DoubleMaStrategy
from datetime import datetime


# In[6]:


#%%
from vnpy_ctastrategy.strategies.dual_thrust_strategy import DualThrustStrategy
from vnpy_ctastrategy.strategies.king_keltner_strategy import KingKeltnerStrategy
from vnpy_ctastrategy.strategies.multi_signal_strategy import MultiSignalStrategy
from vnpy_ctastrategy.strategies.turtle_signal_strategy import TurtleSignalStrategy

engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="600111.SSE",
    interval="d",
    start=datetime(2015, 1, 1),
    end=datetime(2022, 4, 8),
    rate=0.3/10000,
    slippage=0.2,
    size=300,
    pricetick=0.2,
    capital=1_000_000,
)
# engine.add_strategy(AtrRsiStrategy, {})
engine.add_strategy(DoubleMaStrategy, {})
# engine.add_strategy(TurtleSignalStrategy, {})
# engine.add_strategy(MultiSignalStrategy, {"tick_add": -5})  # tick_add表示下单相比信号bar的close加价多少
# engine.add_strategy(DualThrustStrategy, {})

# engine.add_strategy(KingKeltnerStrategy, {})
# engine.add_strategy(BollChannelStrategy, {})


# In[7]:


#%%
engine.load_data()
engine.run_backtesting()
df = engine.calculate_result()
engine.calculate_statistics()
engine.show_chart()


# In[8]:


# setting = OptimizationSetting()
# setting.set_target("sharpe_ratio")
# setting.add_parameter("atr_length", 25, 27, 1)
# setting.add_parameter("atr_ma_length", 10, 30, 10)
#
# engine.run_ga_optimization(setting)


# In[9]:


# engine.run_bf_optimization(setting)


# In[ ]:




