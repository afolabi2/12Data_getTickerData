import pandas as pd 
import json
import getYfData as yfd
import get12Data as g12d
# to run streamlit app
# streamlit run ./files.py/old_testing.py


#print("starting")
#
##symbol = "AACOU"
#symbol = "TSLA"
#x,y,xa,ya = yfd.get_yf_float_outstand_shares(symbol)
#print(x,y,xa,ya)
#
#print("ending")

symbol = 'AAPL'
interval = '5min'
start_date = '2010-06-29'
end_date = '2021-01-29'
#start_date = '2010-06-29 0:00:00'
result = g12d.getStartStopRngeLst(symbol, interval, start_date, end_date)
