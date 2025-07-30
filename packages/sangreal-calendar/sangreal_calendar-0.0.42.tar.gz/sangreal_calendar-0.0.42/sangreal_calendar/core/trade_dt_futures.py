import datetime as dt
from functools import lru_cache

import pandas as pd
from pandas.tseries.offsets import WeekOfMonth

from .refresh_rate_handle import Monthly, Quarterly
from .trade_dt_handle import CALENDAR, adjust_trade_dt, step_trade_dt


@lru_cache()
def get_delistdate_all():
    """[获取交割日]
    """
    M = Monthly(1)
    today = dt.datetime.today().strftime('%Y%m%d')
    delistdate = M.get('20150501', f'{int(today[:4])+2}0101')
    delistdate = pd.to_datetime(delistdate).dt.date + \
        WeekOfMonth(1, week=2, weekday=4)
    delistdate = delistdate[delistdate < pd.to_datetime(
        CALENDAR.dates.iloc[-1])].copy()
    delistdate = delistdate.map(lambda x: adjust_trade_dt(x, adjust='next'))
    delistdate = sorted([d for d in delistdate if d <= M.next(today, 2)])
    return delistdate


@lru_cache()
def get_delistdate_tf_all():
    """[获取交割日] 国债
    """
    M = Monthly(1)
    Q = Quarterly(-1)
    today = dt.datetime.today().strftime('%Y%m%d')
    delistdate = Q.get('20151231', f'{int(today[:4])+2}0101')
    delistdate = delistdate.map(lambda x: step_trade_dt(M.prev(x), -2))
    delistdate = delistdate[delistdate < CALENDAR.dates.iloc[-1]].copy()
    delistdate = sorted([d for d in delistdate if d <= Q.next(today, 2)])
    return delistdate


@lru_cache(maxsize=4)
def get_delistdate(date):
    """[获取交割日]
    """
    M = Monthly(1)
    delistdate = M.get('20150501', M.next(date, 1))
    delistdate = pd.to_datetime(delistdate).dt.date + \
        WeekOfMonth(1, week=2, weekday=4)
    delistdate = delistdate.map(lambda x: adjust_trade_dt(x, adjust='next'))
    if delistdate.iloc[-2] >= date:
        delistdate = delistdate.iloc[:-1].copy()
    return delistdate


@lru_cache(maxsize=4)
def get_contract(date):
    """[获取主力及次主力合约,仅针对股指期货]
    """
    M = Monthly(1)
    contract = []
    delisdate = get_delistdate(date).iloc[-1]
    c0 = delisdate[2:6]
    c1 = M.next(delisdate, 1)[2:6]
    if date == delisdate:
        contract.append(c1)
    elif date > step_trade_dt(delisdate, -4):
        contract.append(c0)
        contract.append(c1)
    else:
        contract.append(c0)
    return pd.Series(contract)
