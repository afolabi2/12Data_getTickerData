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

StringLen10 = '2010-06-29'
DateStrLen19 = g12d.convertDateStrLen10toDateStrLen19(StringLen10)
DateTimeObj1 = g12d.convertDateStrLen10toDateTime(StringLen10)
DateTimeObj2 = g12d.convertDateStrLen10toDateTimeNoHrsMinSecs(StringLen10)
print(f'StringLen10: {StringLen10}')
print(f'DateStrLen19: {DateStrLen19}')
print(f'DateTimeObj1: {DateTimeObj1}')
print(f'DateTimeObj2: {DateTimeObj2}')

print(f'DateTimeObj1 Type: {type(DateTimeObj1)}')
print(f'DateTimeObj2 Type: {type(DateTimeObj2)}')
#result = g12d.getStartStopRngeLst(symbol, interval, start_date, end_date)
