# import statements
import requests, json
import pandas as pd 
import pathlib
from dataclasses import dataclass
from dataclasses import field
from dataclasses import InitVar
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO
from datetime import timedelta
from datetime import date
import time
from time import sleep
import math
import streamlit as st
# **********************************************
# waiting tasks
# **********************************************

#0 this code file is to create a databse for stocks to be studied 
    #next file will update databse
    #next file will analyse databse and proffer recommendations
    #next file will use recommendations and users assent to place waiting orders and alerts
    #all this will be done in streamlit/python
#1 add function to get list of all available stock tickers in 12data
#2 add function to get list of all available crypto tickers in 12data
#3 Filter out preferred stock, american depositry receipts, closed end funds, reit
    #stockTypes = ['PFD','ADR','CEF','MLP','REIT','RIGHT','UNIT','WRT']
#4 confirm timezone to use
#6 confirm with flo if 12data covers satisfactorily all exchanges|all tickers
    #|all crypto exchanges|all crypto pairs|requested required info 



# **********************************************
# inview tasks
# **********************************************
# max nos of rows gettable is 5k per request> https://support.twelvedata.com/en/articles/5214728-getting-historical-data
# use https://sahilramani.com/2021/01/series-how-to-analyze-stock-data-step-1-data-collection/

# **********************************************
# done tasks
# **********************************************
#Now pls check whats in the dataclass df's to confirm data is in it
# confirm if json files produced overwrite or just appends
# get earliest dates a ticker was registered on exchanges: https://twelvedata.com/docs#earliest-timestamp




@dataclass # data class to hold single ticker dataclass object
class singleTickerData(object):
    ticker: str
    interval: str
    start_date: str
    earliestdatetime: str
    earliestUnix_time: str
    df_tsMeta : pd.core.frame.DataFrame
    df_tsData : pd.core.frame.DataFrame
    df_tsError : pd.core.frame.DataFrame
    df_dvMeta : pd.core.frame.DataFrame
    df_dvData : pd.core.frame.DataFrame
    df_dvError : pd.core.frame.DataFrame
    df_spMeta : pd.core.frame.DataFrame
    df_spData : pd.core.frame.DataFrame
    df_spError : pd.core.frame.DataFrame

@dataclass # data class to hold list of ticker dataclass object
class multiTickerData(object):
    listTickerDClass: list
    def populatelist(dcItem):
        listTickerDClass.append(dcItem)

@dataclass # data class to hold input values for each ticker - mostly useless might remove it
class singleTickerInput(object):
    # api keys
    #alpha_vantage_api_key : str = "FYQD4Z70A1KX5QI9"
    twelvedata_api_key: str = "7940a5c7698545e98f6617f235dd1d5d"
    ticker: str = "AAPL"
    interval: str = "1min"
    start_date: str = "2016-01-20"
    end_date: str = ""
    earliestDateTime_data: str = ""
    earliestUnixTime_data: str = ""
    timezone: str = ""   

""" # returns list of calculated start/end time/date that program will run to get complete range of data: 
    use this to circumspect the 5000entries limit per api call
    """
def getStartStopRngeLst(interval, start_date, end_date, timedeltaInMinutes): 
    max_outputsze   = 5000
    timedeltaInSeconds = timedeltaInMinutes * 60
    interval_lst         = ['1min', '5min', '15min', '30min', '45min', '1h', '2h', '4h', '1day', '1week', '1month']
    intervalQty_lst     = [1     ,  5    ,  15    ,  30    ,  45    ,  60 ,  120, 240 ,  1440 ,  10080 ,  44640]
    
    # this is nos of bars within timedeltaInMinutes
    nosBars_lst   = [math.floor((timedeltaInMinutes ) / x) for x in intervalQty_lst] 
    
    # dictionary of mins/bar mapped against interval
    interval_intervalQty_dict = {interval_lst[i]: intervalQty_lst[i] for i in range(len(interval_lst))}
    
    # dictionary of (nos of bar)/timedeltaInMinutes mapped against interval
    interval_nosBars_dict = {interval_lst[i]: nosBars_lst[i] for i in range(len(interval_lst))}
    
    minsPerBar = interval_intervalQty_dict[f'{interval}']
    nosBars = interval_nosBars_dict[f'{interval}']
    
    print(f'total bars: {nosBars} | minutes per bar: {minsPerBar} | total bars * minutes per bar: {nosBars * minsPerBar} | input qty of time: {timedeltaInMinutes}')
    
    # get nos of loop
    loop = math.ceil(nosBars / max_outputsze)
    remnant = nosBars - (max_outputsze * loop)
    print(f'loop: {loop}| remnant: {remnant}')

    if remnant > 0:
        maxloop = loop + 1
    else:
        maxloop = loop
    
    # work on creating list of date pairs
    count = 0
    listStartEndDates = []
    for testloop in range(maxloop):
        if count == 0:
            firsttime = start_date
            curr_seconds_range = minsPerBar * max_outputsze * 60
            secondtime = firsttime + timedelta(seconds=curr_seconds_range)
            lst_entry = [firsttime, firsttime]
            listStartEndDates.append(lst_entry)
            logStartDate = secondtime
        elif (count > 0) and (count < maxloop):
            firsttime = logStartDate
            curr_seconds_range = minsPerBar * max_outputsze * 60
            secondtime = firsttime + timedelta(seconds=curr_seconds_range)
            lst_entry = [firsttime, firsttime]
            listStartEndDates.append(lst_entry)
            logStartDate = secondtime
            if (count == maxloop - 1):
                print(f'count: {count}| start time: {firsttime} | end time {secondtime}')
        count += 1
    return listStartEndDates

# function returns new date from the sum of date and time interval provided
def addTimeDelta(date_str, timeRangeinMinutes):
    date       = datetime.strptime(f'{date_str}', '%Y-%m-%d' '%H:%M:%S')
    curr_seconds_range = timeRangeinMinutes * 60
    time_delta = timedelta(seconds=curr_seconds_range)
    date = date + time_delta
    date_str = date.strftime.strftime('%Y-%m-%d' '%H:%M:%S')
    return date_str, date

# function adds atime interval to a date using relative time delta calculations
def addRelTimeDelta(date, timeIntervalValue, timeIntervalUnit):
    errorcode = 0
    if timeIntervalUnit == "seconds":
        rel_delta = relativedelta(seconds=timeIntervalValue)
    elif timeIntervalUnit == "minutes":
        rel_delta = relativedelta(minutes=timeIntervalValue)
    elif timeIntervalUnit == "hours":
        rel_delta = relativedelta(hours=timeIntervalValue)
    elif timeIntervalUnit == "days":
        rel_delta = relativedelta(days=timeIntervalValue)
    elif timeIntervalUnit == "weeks":
        rel_delta = relativedelta(weeks=timeIntervalValue)
    elif timeIntervalUnit == "months":
        rel_delta = relativedelta(months=timeIntervalValue)
    elif timeIntervalUnit == "years":
        rel_delta = relativedelta(years=timeIntervalValue)
    else:
        errorcode = 1
    
    datetime_object = datetime.strptime(date,  '%Y-%m-%d')
    datetime_object += rel_delta
    new_date = datetime_object.strftime('%Y-%m-%d')
    return new_date






# function returns todays date
def getTodaysDate():
    today_str = datetime.today().strftime('%Y-%m-%d' '%H:%M:%S')
    today = datetime.strptime(f'{today_str}', '%Y-%m-%d' '%H:%M:%S')
    return today_str, today

# function to get date ranges that will be broken down into a list of smaller start/stop pairs
def getDateRange(twelvedata_api_key, ticker, interval,
                timeRangeOption = 'EarliestTimeStamp_TodaysDate',
                user_start_date_str = "", user_end_date_str = "",
                timeRangeinMinutes = ''):
    
    # switches defined by streamlit app
    #timeRangeOption = 'earliestTimeStamp_todaysDate'
    #timeRangeOption = 'earliestTimeStamp_userEndDate'
    #timeRangeOption = 'earliestTimeStamp_timeRange'
    #timeRangeOption = 'userStartDate_todaysDate'
    #timeRangeOption = 'userStartDate_timeRange'
    #timeRangeOption = 'userEndDate_timeRange'
    #timeRangeOption = 'userStartDate_userEndDate'
    
    if timeRangeOption == 'EarliestTimeStamp_TodaysDate':
        # TIMESTAMP
        time_dict = getTickerEarliesrTimeStamp(twelvedata_api_key, ticker, interval)
        start_date_str = time_dict['datetime_data'] 
        start_date = datetime.strptime(f'{start_date_str}', '%Y-%m-%d' '%H:%M:%S') 
        
        # TODAYSDATE
        end_date_str, end_date = getTodaysDate()
        
        # DURATION CALCS.
        duration = end_date - start_date
        diff_in_minutes = duration.total_seconds() / 60
        diff_in_minutes = math.floor(diff_in_minutes)
    
    elif useEarliestTimeStamp == 'earliestTimeStamp_userEndDate':
        # TIMESTAMP
        time_dict = getTickerEarliesrTimeStamp(twelvedata_api_key, ticker, interval)
        start_date_str = time_dict['datetime_data'] 
        start_date = datetime.strptime(f'{start_date_str}', '%Y-%m-%d' '%H:%M:%S') 

        # ENDDATE
        end_date_str  = user_end_date_str
        end_date =  datetime.strptime(f'{end_date_str}', '%Y-%m-%d' '%H:%M:%S')

        # DURATION CALCS.
        duration = end_date - start_date
        diff_in_minutes = duration.total_seconds() / 60
        diff_in_minutes = math.floor(diff_in_minutes)
    
    elif useEarliestTimeStamp == 'earliestTimeStamp_timeRange':
        # TIMESTAMP
        time_dict = getTickerEarliesrTimeStamp(twelvedata_api_key, ticker, interval)
        start_date_str = time_dict['datetime_data'] 
        start_date = datetime.strptime(f'{start_date_str}', '%Y-%m-%d' '%H:%M:%S')
        
        # TIMERANGE
        end_date_str, end_date = addTimeDelta(start_date_str, timeRangeinMinutes)

        # DURATION CALCS.
        duration = end_date - start_date
        diff_in_minutes = duration.total_seconds() / 60
        diff_in_minutes = math.floor(diff_in_minutes)
        print(type(diff_in_minutes))
    
    elif useEarliestTimeStamp == 'userStartDate_todaysDate':
        # STARTDATE
        start_date_str = user_start_date_str 
        start_date = datetime.strptime(f'{start_date_str}', '%Y-%m-%d' '%H:%M:%S')
        
        # TODAYSDATE
        end_date_str, end_date = getTodaysDate()
        
        # DURATION CALCS.
        duration = end_date - start_date
        diff_in_minutes = duration.total_seconds() / 60
        diff_in_minutes = math.floor(diff_in_minutes)
        print(type(diff_in_minutes))
    
    elif useEarliestTimeStamp == 'userStartDate_timeRange':
        # STARTDATE
        start_date_str = user_start_date_str 
        start_date = datetime.strptime(f'{start_date_str}', '%Y-%m-%d' '%H:%M:%S')
        
        # TIMERANGE
        end_date_str, end_date = addTimeDelta(start_date_str, timeRangeinMinutes)
        
        # DURATION CALCS.
        duration = end_date - start_date
        diff_in_minutes = duration.total_seconds() / 60
        diff_in_minutes = math.floor(diff_in_minutes)
        print(type(diff_in_minutes))      

    elif useEarliestTimeStamp == 'userEndDate_timeRange':
        # ENDDATE
        end_date_str = user_end_date_str 
        end_date = datetime.strptime(f'{end_date_str}', '%Y-%m-%d' '%H:%M:%S')
        
        # TIMERANGE
        start_date_str, start_date = addTimeDelta(end_date_str, timeRangeinMinutes)
        
        # DURATION CALCS.
        duration = end_date - start_date
        diff_in_minutes = duration.total_seconds() / 60
        diff_in_minutes = math.floor(diff_in_minutes)
        print(type(diff_in_minutes)) 

    elif useEarliestTimeStamp == 'userStartDate_userEndDate':
        # STARTDATE
        start_date_str = user_start_date_str 
        start_date = datetime.strptime(f'{start_date_str}', '%Y-%m-%d' '%H:%M:%S')

        # ENDDATE
        end_date_str = user_end_date_str 
        end_date = datetime.strptime(f'{end_date_str}', '%Y-%m-%d' '%H:%M:%S')
        
        # DURATION CALCS.
        duration = end_date - start_date
        diff_in_minutes = duration.total_seconds() / 60
        diff_in_minutes = math.floor(diff_in_minutes)
        print(type(diff_in_minutes)) 

    listStartEndDates = getStartStopRngeLst(interval, start_date, end_date, diff_in_minutes)
    return listStartEndDates




    #return diff_in_minutes, start_date_dttime

# function to create folder(nFolder):
def createfolder(nwFolder):
    ii = pathlib.Path(__file__).parent.resolve().parents[0]
    #print(f'{str(ii)} is main directory')
    p = ii / f'{nwFolder}'
    #p = pathlib.Path(f'{nwFolder}/')
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
    #fn = "test.txt" # I don't know what is your fn
    #filepath = p / fn
    #with filepath.open("w", encoding ="utf-8") as f:
        #f.write(data)
    return p

# def function to get earliest timestamp for each stock ticker
def getTickerEarliesrTimeStamp(twelvedata_api_key, ticker, interval):
    data_types = ["earliest_timestamp"]
    #twelvedata_url = f'https://api.twelvedata.com/{data_types}?symbol={ticker}&interval=1day&apikey={twelvedata_api_key}'
    twelvedata_url =  f'https://api.twelvedata.com/earliest_timestamp?symbol={ticker}&interval=1day&apikey={twelvedata_api_key}'
    json_object = requests.get(twelvedata_url).json()
    
    #session = requests.Session()
    ## In case I run into issues, retry my connection
    #retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    #session.mount('http://', HTTPAdapter(max_retries=retries))
    ## Initial request to get the ticker count
    #r = session.get(twelvedata_url)
    #json_object = r.json()

    datetime_data = json_object['datetime']
    unix_time_data = json_object['unix_time']
    mydict = {}
    mydict['datetime_data'] = datetime_data
    mydict['unix_time_data'] = unix_time_data
    return mydict

# get stock ticker main data
def getdata_12data(twelvedata_api_key, ticker, interval, start_date, earliestDateTime_data, earliestUnixTime_data): #do i need to add timezone?
    # TwelveData Work
    data_types = ["time_series", "dividends", "splits"]
    #data_types = ["splits"]
    value_type = ["values", "dividends", "splits"]
    #value_type = ["splits"]

    ## create json.files folder if not exist
    #p = str(createfolder('files.json'))
    #print(f'json files will be stored in {p} folder')

    counter = 0
    # initialise empty dataframes
    tsMeta_df = pd.DataFrame()
    tsData_df = pd.DataFrame()
    tsError_df = pd.DataFrame()
    dvMeta_df = pd.DataFrame()
    dvData_df = pd.DataFrame() 
    dvError_df = pd.DataFrame()
    spMeta_df = pd.DataFrame()
    spData_df = pd.DataFrame() 
    spError_df = pd.DataFrame()

    for data_type in data_types:
        #print("+" * 60) 
        #print(f'working on {data_type} for {ticker} now')
        #print("+" * 60)
        # time series data - adjusted close price
        # ref: https://support.twelvedata.com/en/articles/5179064-are-the-prices-adjusted
        twelvedata_url = f"https://api.twelvedata.com/{data_type}?symbol={ticker}&interval={interval}&start_date={start_date}&apikey={twelvedata_api_key}"
        #json_object = requests.get(twelvedata_url).json()
        
        session = requests.Session()
        # In case I run into issues, retry my connection
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        # Initial request to get the ticker count
        r = session.get(twelvedata_url)
        json_object = r.json()
        
        if ('status' in json_object):
            status_exist = True
        else:
            status_exist = False
        
        if (status_exist == True):
            status_data = json_object['status']

            if status_data == 'ok':
                ##print("")
                #print("=" * 60)
                #print(f'status: {status_data} for {data_type} of {ticker} ticker')
                #print(f'{data_type} data captured from twelvedata api for {ticker} ticker')
                #print("=" * 60)

                meta_data = json_object['meta']
                meta_df = pd.DataFrame(meta_data, index=[0]) # will add start and end dates to meta_df

                value_data = json_object[f'{value_type[counter]}']
                value_df = pd.DataFrame(value_data) # will add start and end dates to meta_df

                #print(meta_df.head(5))
                #print("+" * 60)
                # print(value_data)
                #print(value_df.head(5))

                # creation of json file for files with status ok
                #mypath = pathlib.Path(f'{p}', f'{ticker}_{data_type}.json')
                #with open(mypath, "w") as outfile:
                #    json.dump(json_object, outfile)
                
                if data_type == "time_series":
                    tsMeta_df = meta_df
                    tsData_df = value_df

                elif data_type == "dividends":
                    dvMeta_df = meta_df
                    dvData_df = value_df 
                    
                elif data_type == "splits":
                    spMeta_df = meta_df
                    spData_df = value_df 
               
            elif status_data == 'error':
                code_data = json_object['code']
                mess_data = json_object['message']
                ##print("")
                #print("=" * 60)
                #print(f'{data_type} data error from twelvedata api for {ticker} stock')
                #print(f'error code:{code_data} | message: {mess_data}')
                #print("=" * 60)

                

                error_data = json_object
                error_df = pd.DataFrame(json_object, index=[0]) 

                if data_type == "time_series":
                    tsError_df = error_df

                elif data_type == "dividends":
                    dvError_df = error_df
                    
                elif data_type == "splits":
                    spError_df = error_df

                # creation of json file for files with status error
                #mypath = pathlib.Path(f'{p}', f'{ticker}_{data_type}_error.json')
                #with open(mypath, "w") as outfile:
                #    json.dump(json_object, outfile)

        elif (status_exist == False):
            ##print("")
            #print("=" * 60)
            #print(f'{data_type} data from twelvedata api for {ticker} stock')
            #print("=" * 60)

            meta_data = json_object['meta']
            meta_df = pd.DataFrame(meta_data, index=[0]) # will add start and end dates to meta_df


            #print('+' * 60)
            #print(f'{value_type[counter]}')
            #print(f'{data_type}')
            #print(f'{counter}')
            value_data = json_object[f'{value_type[counter]}']
            value_df = pd.DataFrame(value_data) 

            #print(meta_df.head(5))
            #print("+" * 60)
            # print(value_data)
            #print(value_df.head(5))

            # creation of json file for files with no status
            #mypath = pathlib.Path(f'{p}', f'{ticker}_{data_type}.json')
            #with open(mypath, "w") as outfile:
            #    json.dump(json_object, outfile)

            if data_type == "time_series":
                tsMeta_df = meta_df
                tsData_df = value_df

            elif data_type == "dividends":
                dvMeta_df = meta_df
                dvData_df = value_df 
                    
            elif data_type == "splits":
                spMeta_df = meta_df
                spData_df = value_df 
                
        counter += 1
        ticker_dc = singleTickerData(ticker=ticker, 
                                    interval=interval,
                                    start_date=start_date,
                                    earliestdatetime=earliestDateTime_data,
                                    earliestUnix_time=earliestUnixTime_data,
                                    df_tsMeta=tsMeta_df, 
                                    df_tsData=tsData_df,
                                    df_tsError=tsError_df, 
                                    df_dvMeta=dvMeta_df,
                                    df_dvData=dvData_df,
                                    df_dvError=dvError_df,
                                    df_spMeta=spMeta_df,
                                    df_spData=spData_df,
                                    df_spError=spError_df
                                                ) 
    # check ticker_dc contents
    print("=" * 80)
    print(f'ticker check for {ticker_dc.ticker}')
    print(f'ticker interval is {ticker_dc.interval}')
    print(f'ticker stock data from date {ticker_dc.start_date}')
    print(f'Earliest Date-time for {ticker_dc.ticker} is {ticker_dc.earliestdatetime}')
    print(f'Earliest Unix-time for {ticker_dc.ticker} is {ticker_dc.earliestUnix_time}')
    print(f'column qty of df_tsMeta is {len(ticker_dc.df_tsMeta.index)}') 
    print(f'column qty of df_tsData is {len(ticker_dc.df_tsData.index)}') 
    print(f'column qty of df_tsError is {len(ticker_dc.df_tsError.index)}') 
    print(f'column qty of df_dvMeta is {len(ticker_dc.df_dvMeta.index)}') 
    print(f'column qty of df_dvData is {len(ticker_dc.df_dvData.index)}') 
    print(f'column qty of df_dvError is {len(ticker_dc.df_dvError.index)}') 
    print(f'column qty of df_spMeta is {len(ticker_dc.df_spMeta.index)}') 
    print(f'column qty of df_spData is {len(ticker_dc.df_spData.index)}')   
    print(f'column qty of df_spError is {len(ticker_dc.df_spError.index)}')    
    print("=" * 80)                                   
    return ticker_dc

def returnTickerLst():
    #Tickers = ['brtx','gree','sxtc',
    #     'VCF','NVEC','CPHC','OVBC','LARK','BOTJ','CHMG','USEG','UG',
    #     'SYTA','ARTW','VFL','UNB','ALAC','HMNF','WAFU','AEHL','GFED',
    #     'OPHC','OPNT','WSTG','SGMA','AE','EGF','FMY','INDP','CSPI','IOR',
    #     'NATH','LLL', 'RMED','GRF','LEDS','DXR','HIHO','MRM','AHPI','DTST',
    #     'PNBK','NXN','AWX','STRT','ISDR','SMIT','ALTM','NEN','PDEX','UTMD',
    #     'NWLI','WINA', 'DUOT','NVR','CFFI','ACU','AUBN','ARKR','ESBK','CARV',
    #     'TAYD','JCTCF','AGIL','PATI','ELSE','FCAP','TRT','PW','UBOH','FFHL',
    #     'RMBL','HFBL', 'DHIL','PFIN','SBET','WTM','IROQ','LTRPB','HSON','BBLG',
    #     'AIRT','MSVB','GLBZ','JAN','SAL','SVFD','AINC','KEQU','EMCF','LRFC',
    #     'PFX','NSYS','EDRY','SZC','SFBC','RAND','CLWT','NSEC','KSPN','GBNY',
    #     'BCACU','RBCN','ESP','SVT','NCSM','NOM','SNOA','HSDT','UUU','JRJC',
    #     'TTP','INTG','SRV','SUMR','HIFS','MXC','FEMY','BH','AAMC','MAYS','PNRG',
    #     'MARPS','IKNX','TSRI','CKX','MTEX','ITIC','MTR','BDL','NDP','RHE','ATRI',
    #     'MXE','ISIG','WVFC','BHV','LIVE','ACY','CNTX','GYRO','VBFC','DJCO','COHN',
    #     'SEB','CVR','BRTX','DIT','mitq'
    #      ]
    Tickers = ['brtx','gree','sxtc']
    return Tickers

# main program controlling logic
def main_run():
    tickerlst = returnTickerLst()
    TickerDCLst = []
    multiTickerDCLst = []
    for ticker in tickerlst:
        # api keys
        #alpha_vantage_api_key = "FYQD4Z70A1KX5QI9"
        twelvedata_api_key = "7940a5c7698545e98f6617f235dd1d5d"
        #ticker: str = "AAPL"
        interval = "1min"
        start_date = "2016-01-20"
        end_date = ""
        timezone = ""
        
        useEarliestTimeStamp = True
        earliestTimeStampDct = getTickerEarliesrTimeStamp(twelvedata_api_key, ticker, interval)
        earliestDateTime_data  = earliestTimeStampDct['datetime_data']
        earliestUnixTime_data  = earliestTimeStampDct['unix_time_data']

        if useEarliestTimeStamp == True:
            start_date  = earliestDateTime_data

        singleTickerDC = singleTickerInput(twelvedata_api_key, ticker, interval, start_date, end_date, earliestDateTime_data, earliestUnixTime_data, timezone )
        TickerDCLst.append(singleTickerDC)
        
       
    for tickerdata in TickerDCLst:
        single_ticker_dc = getdata_12data(tickerdata.twelvedata_api_key, tickerdata.ticker, tickerdata.interval, tickerdata.start_date, 
                                            tickerdata.earliestDateTime_data, tickerdata.earliestUnixTime_data)
        #sleep(10)
        multiTickerDCLst.append(single_ticker_dc)

    multi_ticker_dc = multiTickerData(listTickerDClass = multiTickerDCLst)

def tester():
         # api keys
        #alpha_vantage_api_key = "FYQD4Z70A1KX5QI9"
        twelvedata_api_key = "7940a5c7698545e98f6617f235dd1d5d"
        ticker: str = "gree"
        interval = "5min"

        
        # switches defined by streamlit app
        #timeRangeOption = 'earliestTimeStamp_todaysDate'
        #timeRangeOption = 'earliestTimeStamp_userEndDate'
        #timeRangeOption = 'earliestTimeStamp_timeRange'
        #timeRangeOption = 'userStartDate_todaysDate'
        #timeRangeOption = 'userStartDate_timeRange'
        #timeRangeOption = 'userEndDate_timeRange'
        #timeRangeOption = 'userStartDate_userEndDate'

        #assumed value of timeRangeOption from steamlit
        timeRangeOption = 'userStartDate_timeRange' 
        
        if timeRangeOption == 'EarliestTimeStamp_TodaysDate':
            # this data will come from streamlit input
            timezone = ""
            lstDateRnge = getDateRange(twelvedata_api_key, ticker, interval, 
                        timeRangeOption = 'EarliestTimeStamp_TodaysDate')
       
        elif timeRangeOption == 'earliestTimeStamp_userEndDate':
           # this data will come from streamlit input
            timezone = ""
            end_date = "2021-12-27"
            lstDateRnge = getDateRange(twelvedata_api_key, ticker, interval, 
                                        timeRangeOption = 'earliestTimeStamp_userEndDate', 
                                        user_end_date_str = end_date)

        elif timeRangeOption == 'earliestTimeStamp_timeRange':
           # this data will come from streamlit input
            timezone = ""
            timeRangeinMinutes = 15000
            lstDateRnge = getDateRange(twelvedata_api_key, ticker, interval, 
                                        timeRangeOption = 'earliestTimeStamp_timeRange', 
                                        timeRangeinMinutes = timeRangeinMinutes)

        elif timeRangeOption == 'userStartDate_todaysDate':
           # this data will come from streamlit input
            timezone = ""
            start_date = "2021-12-27"
            lstDateRnge = getDateRange(twelvedata_api_key, ticker, interval, 
                                        timeRangeOption = 'userStartDate_todaysDate', 
                                        user_start_date_str = start_date)

        elif timeRangeOption == 'userStartDate_timeRange':
            # this data will come from streamlit input
            timezone = ""
            start_date = "2021-12-27"
            timeRangeinMinutes = 15000
            lstDateRnge = getDateRange(twelvedata_api_key, ticker, interval, 
                                        timeRangeOption = 'userStartDate_timeRange', 
                                        user_start_date_str = start_date, 
                                        timeRangeinMinutes = timeRangeinMinutes)

        elif timeRangeOption == 'userEndDate_timeRange':
            # this data will come from streamlit input
            timezone = ""
            end_date = "2021-12-27"
            timeRangeinMinutes = 15000
            lstDateRnge = getDateRange(twelvedata_api_key, ticker, interval, 
                                        timeRangeOption = 'userEndDate_timeRange', 
                                        user_end_date_str = end_date, 
                                        timeRangeinMinutes = timeRangeinMinutes)
        
        elif timeRangeOption == 'userStartDate_userEndDate':
            # this data will come from streamlit input
            timezone = ""
            start_date = "2021-10-27"
            end_date = "2021-12-27"
            lstDateRnge = getDateRange(twelvedata_api_key, ticker, interval, 
                                        timeRangeOption = 'userEndDate_timeRange', 
                                        user_start_date_str = start_date, user_end_date_str = end_date)

#getDateRange(twelvedata_api_key, ticker, interval,
                #timeRangeOption = 'EarliestTimeStamp_TodaysDate',
                #user_start_date_str = "", user_end_date_str = "",
                #timeRangeinMinutes = ''):



# logic runner
if __name__ == "__main__":
    print ("Executing main Program Now")
    #main_run()
    tester()
    
else:
    print ("Executed when imported")