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
interval = '30min'
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
print(f'Time Series Data will be extracted for {len(symb_timeRnge_df.index)} time intervals')

tcker_dc_lst = g12d.getSymbolTimeSeries_dfs(twelvedata_api_key, symb_timeRnge_df)



#print(f'total number of time series data to reduce to one data is {len(tcker_dc_lst)}')
#
#cnter = 0
#for tcker_dc in tcker_dc_lst:
#    if cnter == 0:
#        chk_ticker              = ticker_dc.ticker
#        chk_interval            = ticker_dc.interval
#        chk_start_date          = ticker_dc.start_date
#        chk_outputsize          = ticker_dc.outputsize
#        chk_status_message      = ticker_dc.status_message
#        first_dc_tsMeta    = ticker_dc.df_tsMeta
#        first_dc_tsData    = ticker_dc.df_tsData
#        first_dc_tsError   = ticker_dc.df_tsError
#    else:
#        passchk = 1
#        if not chk_ticker == ticker_dc.ticker:
#            passchk = 0
#        if not chk_interval == ticker_dc.interval:
#            passchk = 0
#        if not chk_start_date == ticker_dc.start_date:
#            passchk = 0
#        if not chk_outputsize == ticker_dc.outputsize:
#            passchk = 0
#        if not chk_status_message == ticker_dc.status_message:
#            passchk = 0
#        
#        if passchk == 1:
#            pass
#        else:
#           print(f" we have a bad dataclass in the list @ {cnter} position")
#           st.write(f" we have a bad dataclass in the list @ {cnter} position")
