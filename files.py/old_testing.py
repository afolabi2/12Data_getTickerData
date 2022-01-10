import pandas as pd 
import json
import getYfData as yfd
import get12Data as g12d
from time import sleep
import streamlit as st
# to run streamlit app
# streamlit run ./files.py/old_testing.py


twelvedata_api_key = '7940a5c7698545e98f6617f235dd1d5d'
ticker = 'AAPL'
interval = '5min'
data_pts = 4500
start_date_str = '2010-06-29'
end_date_str = '2021-01-29'

mydict = g12d.getTickerEarliesrTimeStamp(twelvedata_api_key, ticker)
earliesrTimeStamp_str = mydict['datetime_data']
earliesrTimeStamp_unix = mydict['unix_time_data']

# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
from datetime import datetime
ts = int(earliesrTimeStamp_unix)
earliesrTimeStamp_from_unix_to_str = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

print(f'earliesrTimeStamp_str: {earliesrTimeStamp_str}')
print(f'earliesrTimeStamp_from_unix_to_str: {earliesrTimeStamp_from_unix_to_str}')

start_date_dt = g12d.convertDateStrLen10toDateTime(start_date_str)
end_date_dt = g12d.convertDateStrLen10toDateTime(end_date_str)

symb_timeRnge_df, maxRequestPerDay_freekey = g12d.getStartStopRngeLst(ticker, interval, start_date_dt, end_date_dt)
print(f'Time Series Data will be done {len(symb_timeRnge_df.index)} times')

tcker_dc_lst = []
cnt = 1
for indx in symb_timeRnge_df.index:
    ticker = symb_timeRnge_df['symbol'][indx]
    start_time = symb_timeRnge_df['start_time'][indx]
    end_time = symb_timeRnge_df['end_time'][indx]
    interval = symb_timeRnge_df['interval'][indx]
    data_pts = symb_timeRnge_df['data_pts_limit'][indx]
    ticker_dc = g12d.get_TimeSeries_12Data(twelvedata_api_key, ticker, interval, start_time, data_pts)
    tcker_dc_lst.append(ticker_dc)
    
    # get output of data
    dc_ticker       = ticker_dc.ticker
    dc_interval     = ticker_dc.interval
    dc_start_date   = ticker_dc.start_date
    dc_outputsize   = ticker_dc.outputsize
    dc_status_message   = ticker_dc.status_message
    df_dc_tsMeta    = ticker_dc.df_tsMeta
    df_dc_tsData    = ticker_dc.df_tsData
    df_dc_tsError   = ticker_dc.df_tsError

    # check ticker_dc contents
    print("=" * 80)
    print(f"{cnt} of {len(symb_timeRnge_df.index)} Loops")
    print("=" * 80)
    print(f'ticker check for {dc_ticker}')
    print(f'ticker interval is {dc_interval}')
    print(f'ticker stock data from date {dc_start_date}')
    print(f'output size/data points {dc_outputsize}')
    print(f'status message {dc_status_message}')
    print(f'column qty of df_tsMeta is {len(df_dc_tsMeta.index)}')
    print(f'column qty of df_tsData is {len(df_dc_tsData.index)}')
    print(f'column qty of df_tsError is {len(df_dc_tsError.index)}')
    print("*" * 60)
    cnt +=1
    if dc_status_message == 'error':
        aaaaaaaaa
    if dc_status_message == 'status key not exist':
        fggjgjjj
    sleep(5)


print(f'total number of time series data to reduce to one data is {len(tcker_dc_lst)}')
