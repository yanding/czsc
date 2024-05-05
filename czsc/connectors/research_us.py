# -*- coding: utf-8 -*-
"""
author: zengbin93
email: zeng_bin8888@163.com
create_dt: 2023/3/5 20:45
describe: CZSC投研数据共享接口

投研数据共享说明（含下载地址）：https://s0cqcxuy3p.feishu.cn/wiki/wikcnzuPawXtBB7Cj7mqlYZxpDh
"""
import os
import czsc
import glob
import pandas as pd
import os
import sys
# Your data structure as a list of dictionaries
data = [
    {'stock_symbol': 'SPY', 'tf': '1M', 'strategy_type': 'VolBIDASK','freq': '1分钟'},
    {'stock_symbol': 'SPY', 'tf': '5M', 'strategy_type': 'VolBIDASK','freq': '5分钟'},
    {'stock_symbol': 'SPY', 'tf': '30M', 'strategy_type': 'VolBIDASK','freq': '30分钟'},
    {'stock_symbol': 'SPY', 'tf': '60M', 'strategy_type': 'VolBIDASK','freq': '60分钟'},
    {'stock_symbol': 'SPY', 'tf': '30M', 'strategy_type': 'Breadth','freq': '30分钟'},
    {'stock_symbol': 'SPY', 'tf': '60M', 'strategy_type': 'Breadth','freq': '60分钟'},
    {'stock_symbol': 'SPY', 'tf': '30M', 'strategy_type': 'DayCumBreadth','freq': '30分钟'},
    {'stock_symbol': 'SPY', 'tf': '60M', 'strategy_type': 'DayCumBreadth','freq': '60分钟'},
    {'stock_symbol': '$ADSPD', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': '$ADVN', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': '$DECN', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': '$DVOL', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': '$PCSP', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': '$SPXA50R', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': '$SPXA100R', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': '$SPXA200R', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': '$TICK', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': '$TIKSP', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': '$UVOL', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': '$VOLD', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': '$VOLSPD', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': 'UVXY', 'tf': '1M', 'strategy_type': 'VolBIDASK','freq': '1分钟'},
    {'stock_symbol': 'VIX', 'tf': '1M', 'strategy_type': 'BIDASK','freq': '1分钟'},
    {'stock_symbol': 'VXX', 'tf': '1M', 'strategy_type': 'VolBIDASK','freq': '1分钟'},
]
SYMBOLS=set(record['stock_symbol'] for record in data)


# def process_tos_weekly_update_per_year(tos_update_folder, output_folder,data=data):
# # Accessing elements in the list of dictionaries
#     for entry in data:
#         # Accessing values in each dictionary
#         for key, value in entry.items():
#             print(f"{key}: {value}")
#         process_tos_weekly_update_per_symbol_per_strategy_per_year(tos_update_folder, output_folder,symbol=entry['stock_symbol'],timeframe=entry['tf'],strategy_type=entry['strategy_type'])



# 投研共享数据的本地缓存路径，需要根据实际情况修改
cache_path = os.environ.get('czsc_research_cache', r"D:\data\tos")
if not os.path.exists(cache_path):
    raise ValueError(f"请设置环境变量 czsc_research_cache 为投研共享数据的本地缓存路径，当前路径不存在：{cache_path}。\n\n"
    )

def get_symbols(name='ALL',symbols=SYMBOLS, **kwargs):
    """获取指定分组下的所有标的代码

    :param name: 分组名称，可选值：'A股主要指数', 'A股场内基金', '中证500成分股', '期货主力'
    :param kwargs:
    :return:
    """
    # Extract unique symbols

    return list(symbols)

def get_timeframes(data, symbol="SPY", freq='1分钟', strategy_type='VolBIDASK'):
    # Filter data based on provided parameters
    filtered_data = [record['tf'] for record in data if
                     record['stock_symbol'] == symbol and record['freq'] == freq and record['strategy_type'] == strategy_type]

    return filtered_data[0]

def get_raw_bars(symbol="SPY",freq='1分钟',sdt="2021-01-01", edt="2024-01-01", fq='前复权',
                 strategy_type='VolBIDASK',data=data, **kwargs):
    """获取 CZSC 库定义的标准 RawBar 对象列表

    :param symbol: 标的代码
    :param freq: 周期，支持 Freq 对象，或者字符串，如
            '1分钟', '5分钟', '15分钟', '30分钟', '60分钟', '日线', '周线', '月线', '季线', '年线'
    :param sdt: 开始时间
    :param edt: 结束时间
    :param fq: 除权类型，投研共享数据默认都是后复权，不需要再处理
    :param strategy_type: strategy_type, such as 'VolBIDASK'
    :param kwargs:
    :return:
    """
    kwargs['fq'] = fq
    timeframe=get_timeframes(data,symbol,freq,strategy_type)
    file = glob.glob(os.path.join(cache_path, f"{symbol}_{timeframe}_{strategy_type}.csv"))[0]
    freq = czsc.Freq(freq)
    kline = pd.read_csv(file)
    kline.loc[:, 'vol'] = kline['volume']
    kline.loc[:, 'amount'] = kline['close'] * kline['vol']
    if 'dt' not in kline.columns:
        kline['dt'] = pd.to_datetime(kline['datetime'])
    kline['dt'] = pd.to_datetime(kline['dt'],utc=True).dt.tz_localize(None)
    # kline = kline[(kline['dt'] >= pd.to_datetime(sdt).tz_localize('UTC').tz_convert('EST')) & (kline['dt'] <= pd.to_datetime(edt).tz_localize('UTC').tz_convert('EST'))]
    kline = kline[(kline['dt'] >= pd.to_datetime(sdt)) & (kline['dt'] <= pd.to_datetime(edt))]
    if kline.empty:
        return []
    _bars = czsc.resample_bars(kline, freq, raw_bars=True, base_freq='1分钟')
    return _bars
