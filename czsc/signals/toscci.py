# -*- coding: utf-8 -*-
"""
author: Yan Ding
create_dt: 2024/4/28
describe: tos_woodie_cci
"""
from loguru import logger
try:
    import talib as ta
except:
    logger.warning("ta-lib 没有正确安装，相关信号函数无法正常执行。"
                   "请参考安装教程 https://blog.csdn.net/qaz2134560/article/details/98484091")
import numpy as np
import pandas as pd
from typing import List
from collections import OrderedDict
from czsc.analyze import CZSC, RawBar
from czsc.utils.sig import get_sub_elements, create_single_signal
from czsc.signals.tas import update_ma_cache, update_sar_cache, update_kdj_cache, update_cci_cache

from stock_indicators import Quote
from stock_indicators import indicators
import math


def crossed_above(arr1: np.ndarray, num: int, wait: int = 0) -> np.ndarray:
    """Get the crossover of the first array going above the specified number."""
    out = np.empty_like(arr1, dtype=bool)
    was_below = False
    crossed_ago = -1
    for i in range(arr1.shape[0]):
        if np.isnan(arr1[i]):
            crossed_ago = -1
            was_below = False
            out[i] = False
        elif arr1[i] > num:
            if was_below:
                crossed_ago += 1
                out[i] = crossed_ago == wait
            else:
                out[i] = False
        elif arr1[i] == num:
            crossed_ago = -1
            out[i] = False
        else:
            crossed_ago = -1
            was_below = True
            out[i] = False
    return out

def crossed_below(arr1: np.ndarray, num: int, wait: int = 0) -> np.ndarray:
    """Get the crossover of the first array going below the second array."""
    out = np.empty(arr1.shape, dtype=np.bool_)
    was_above = False
    crossed_ago = -1
    for i in range(arr1.shape[0]):
        if np.isnan(arr1[i]):
            crossed_ago = -1
            was_above = False
            out[i] = False
        elif arr1[i] < num:
            if was_above:
                crossed_ago += 1
                out[i] = crossed_ago == wait
            else:
                out[i] = False
        elif arr1[i] == num:
            crossed_ago = -1
            out[i] = False
        else:
            crossed_ago = -1
            was_above = True
            out[i] = False
    return out


def get_count(cci,  start_cutoff=0, continue_cutoff=0,reset_cutoff=0):
    # Initialize Count series with zeros
    Count = pd.Series(0, index=cci.index)

    for i in range(1, len(cci)):
        if cci.iloc[i] < reset_cutoff:
            Count.iloc[i] = 0
        elif Count.iloc[i - 1] == 0 and cci.iloc[i] > start_cutoff:
            Count.iloc[i] = 1
        elif Count.iloc[i - 1] > 0 and cci.iloc[i] > continue_cutoff:
            Count.iloc[i] = Count.iloc[i - 1] + 1
        else:
            Count.iloc[i] = Count.iloc[i - 1]

    return Count

def get_dataframe(c: CZSC, **kwargs):
    """get quotes for stock_indicator
    :param c: CZSC对象
    :return:quotes
    """
    bars=c.bars_raw
    data = {
        'datetime': np.array([x.dt for x in bars])
        'open': np.array([x.open for x in bars]),
        'high': np.array([x.high for x in bars]),
        'low': np.array([x.low for x in bars]),
        'close': np.array([x.close for x in bars]),
        'volume': np.array([x.vol for x in bars])
    }
    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

def get_quotes(c: CZSC, **kwargs):
    """get quotes for stock_indicator
    :param c: CZSC对象
    :return:quotes
    """
    df=get_dataframe(c)
    quotes = [
        Quote(d,o,h,l,c,v) 
        for d,o,h,l,c,v 
        in zip(df['datetime'], df['open'], df['high'], df['low'], df['close'], df['volume'])
    ]
    return(quotes)

def get_cci(c: CZSC, **kwargs):
    """stock_indicators.get_cci

    CCI = (TP - MA) / MD / 0.015; 其中，
    - TP=(最高价+最低价+收盘价)÷3;
    - MA=最近N日收盘价的累计之和÷N;
    - MD=最近N日（MA－收盘价）的累计之和÷N;
    - 0.015为计算系数，N为计算周期

    :param c: CZSC对象
    :return:
    """
    timeperiod = int(kwargs.get('timeperiod', 14))
    quotes =get_quotes(c)
    results = indicators.get_cci(quotes, timeperiod)
    cci=[r.cci for r in results]
    index=[r.date for r in results]
    cci_series = pd.Series(cci, index=index)
    return cci_series


def get_ema(c: CZSC, **kwargs):
    """stock_indicators.get_cci

    CCI = (TP - MA) / MD / 0.015; 其中，
    - TP=(最高价+最低价+收盘价)÷3;
    - MA=最近N日收盘价的累计之和÷N;
    - MD=最近N日（MA－收盘价）的累计之和÷N;
    - 0.015为计算系数，N为计算周期

    :param c: CZSC对象
    :return:
    """
    timeperiod = int(kwargs.get('timeperiod', 34))
    quotes =get_quotes(c)
    results = indicators.get_ema(quotes, timeperiod);
    ema=[r.ema for r in results]
    index=[r.date for r in results]
    ema_series = pd.Series(ema, index=index)
    return ema_series

def get_diff(c: CZSC, **kwargs):
    """stock_indicators.get_cci

    CCI = (TP - MA) / MD / 0.015; 其中，
    - TP=(最高价+最低价+收盘价)÷3;
    - MA=最近N日收盘价的累计之和÷N;
    - MD=最近N日（MA－收盘价）的累计之和÷N;
    - 0.015为计算系数，N为计算周期

    :param c: CZSC对象
    :return:
    """
    timeperiod = int(kwargs.get('timeperiod', 34))
    df =get_dataframe(c)
    ema=get_ema(c)
    diff=df['close']-ema
    return diff

def toscci_bullZLR_V05042024(c: CZSC, **kwargs) -> OrderedDict:
    """CCI Signal bullZLR

    参数模板："{freq}_D{di}CCI{cci_n}#TCCI{tcci_n}_BSV05042024"

     **信号逻辑：**

    1. CCI大于100，且向上突破均线，看多；
    2. CCI小于-100，且向下突破均线，看空；

    **信号列表：**

    - Signal('30分钟_D1CCI20#SMA#5_BS辅助V230323_多头_向上_任意_0')

    :param c: CZSC对象
    :param kwargs: 参数字典
        - :param di: 信号计算截止倒数第i根K线
        - :param tcci_n: TCCI的计算周期
        - :param cci_n: CCI的计算周期
    :return: 返回信号结果
    """
    di = int(kwargs.get("di", 1))
    tcci_n = int(kwargs.get("tcci_n", 6))
    cci_n = int(kwargs.get("cci_n", 14))
    tcci=get_cci(c,timeperiod=tcci_n)
    tcci_shift_1=tcci.shift(1)
    tcci_shift_2=tcci.shift(2)
    cci=get_cci(c,timeperiod=cci_n)
    tcci_cross_above_N100=crossed_above(tcci,-100)
    diff = get_diff(c)
    cciGreenTrendCount=get_count(cci,200,0,-60)
    cciGreenCount=get_count(cci,0,0,0)

    k1, k2, k3 = f"{freq}_D{di}CCI{n}#{ma_type}#{m}_BS辅助V230323".split('_')
    v1 = '其他'
    if tcci_cross_above_N100 and diff>0 and (tcci_shift_1 < -130 or tcci_shift_2 <-130) 
         and ((cci-cci.shift(1)) >-15 or (tcci-tcci_shift_1>=70))
         and cciGreenTrendCount >12
        v1 = '多头'

    if v1 == '其他':
        return create_single_signal(k1=k1, k2=k2, k3=k3, v1=v1)

    v2 = "向上" if cciGreenCount else "向下"
    return create_single_signal(k1=k1, k2=k2, k3=k3, v1=v1, v2=v2)

