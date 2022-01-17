import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import json
import pandas as pd
import numpy as np
import pathlib
import streamlit as st
import getYfData as yfd
from time import sleep
import time
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta, MO
import math

from dataclasses import dataclass
from dataclasses import field
from dataclasses import InitVar

# ====================
# WAITING TASKS
# ====================
#add json object checker to all api json calls 
#label every step in functions
# reduce nested loops to shorter line code
#correct outout size for last dc
# ====================
# DATACLASS FUNCTIONS
# ====================
@dataclass  # data class to hold single ticker dataclass object
class singleTickerData(object):
    ticker: str
    interval: str
    start_date: str
    end_date: str
    outputsize: int
    df_tsMeta: pd.core.frame.DataFrame
    df_tsData: pd.core.frame.DataFrame


@dataclass  # data class to hold list of ticker dataclass object
class multiTickerData(object):
    listTickerDClass: list

    def populatelist(dcItem):
        listTickerDClass.append(dcItem)

@dataclass  # data class to hold input values for each ticker - mostly useless might remove it
class singleTickerInput(object):
    # api keys
    #alpha_vantage_api_key : str = "FYQD4Z70A1KX5QI9"
    twelvedata_api_key: str = "69287070d2f24f60a821b96ec1281011"
    ticker: str = "AAPL"
    interval: str = "1min"
    start_date: str = "2016-01-20"
    end_date: str = ""
    earliestDateTime_data: str = ""
    earliestUnixTime_data: str = ""
    timezone: str = ""

# ====================
# TEXT FORMATTING FUNCTIONS
# ====================

# ====================
# HELPER FUNCTIONS
# ====================
# function to create folder(nFolder):
def createfolder(nwFolder):
    ii = pathlib.Path(__file__).parent.resolve().parents[0]
    #print(f'{str(ii)} is main directory')
    p = ii / f'{nwFolder}'
    #p = pathlib.Path(f'{nwFolder}/')
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
    # fn = "test.txt" # I don't know what is your fn
    #filepath = p / fn
    # with filepath.open("w", encoding ="utf-8") as f:
        # f.write(data)
    return p

# function to confirm a json key/pair exists
def chk_json_key_exists(json_key, json_object):
    if (json_key in json_object):
        json_key_exist = True
    else:
        json_key_exist = False
    return json_key_exist

# create json.files folder  if not exist and dump json file in ot
def dumpjsonData(filename, json_object):
    p = str(createfolder('files.json'))
    print(f'json files will be stored in {p} folder')

    # creation of json file for files with status ok
    mypath = pathlib.Path(f'{p}', f'{filename}.json')
    with open(mypath, "w") as outfile:
        json.dump(json_object, outfile, indent=4, sort_keys=True)

# convert json key/pair to df if status key is "ok"
def get_tck_apistocks_json_df(json_object, status_hdr='status', json_key='data'):
    status_hdr_exist = chk_json_key_exists(
        json_key=status_hdr, json_object=json_object)
    data_df = pd.DataFrame()
    if (status_hdr_exist == True):
        status_hdr_data = json_object[status_hdr]
        if status_hdr_data == 'ok':
            json_key_data = json_object[json_key]
            data_df = pd.DataFrame(json_key_data)
    return data_df

# get ticker stats: shares float and outstanding from 12data statistics api call 
def get_tck_stats_items(apikey_12Data, symbol):
    data_type = "statistics"
    apikey = apikey_12Data
    twelvedata_url = f'https://api.twelvedata.com/{data_type}?symbol={symbol}&apikey={apikey}'
    json_object = requests.get(twelvedata_url).json()
    
    json_object = chkJsonObj(json_object)

    statistics_exists = chk_json_key_exists(
        json_key="statistics", json_object=json_object)

    if statistics_exists:
        json_object = json_object["statistics"]
        stock_statistics_exists = chk_json_key_exists(
            json_key="stock_statistics", json_object=json_object)
        if stock_statistics_exists:
            json_object = json_object["stock_statistics"]
            shares_outstand_data = json_object["shares_outstanding"]
            float_shares_data = json_object["float_shares"]
            return shares_outstand_data, float_shares_data
    else:
        # we wont get data if we dont have a premium 12data subscription, go get data from yfinanace
        shares_outstand_data, float_shares_data, error_out_shre, error_flt_shre = yfd.get_yf_float_outstand_shares(
            symbol)
        return shares_outstand_data, float_shares_data, error_out_shre, error_flt_shre

# get ticker stats: shares float and outstanding from yfinance 
def get_tck_stats_items_from_yFin(symbol):
    shares_outstand_data, float_shares_data, error_out_shre, error_flt_shre = yfd.get_yf_float_outstand_shares(
        symbol)
    return shares_outstand_data, float_shares_data, error_out_shre, error_flt_shre

# get ticker stocks df: list of tickers from 12data statistics api call 
# @st.cache
def get_tck_stocks_df(apikey_12Data):
    data_type = "stocks"
    apikey = apikey_12Data
    twelvedata_url = f'https://api.twelvedata.com/{data_type}'
    json_object = requests.get(twelvedata_url).json()

    json_object = chkJsonObj(json_object)

    #types_stocks = ['EQUITY', 'Common', 'Common Stock', 'American Depositary Receipt',
    #                'Real Estate Investment Trust (REIT)', 'Unit', 'GDR', 'Closed-end Fund',
    #                'ETF', 'Depositary Receipt', 'Preferred Stock', 'Limited Partnership',
    #                'OTHER_SECURITY_TYPE', 'Warrant', 'STRUCTURED_PRODUCT', 'Exchange-traded Note',
    #                'Right', 'FUND', 'Trust', 'Index', 'Unit Of Beneficial Interest',
    #                'MUTUALFUND', 'New York Registered Shares']

    data_df = get_tck_apistocks_json_df(
        json_object, status_hdr='status', json_key='data')
    return data_df

# get ticker name series: from imported df -called from combine_stock_stats_items
def get_tcker_symbol_lst(data_df):
    symbol_lst = sorted(data_df["symbol"].unique())
    return symbol_lst

# get ticker type series: from imported df -called from combine_stock_stats_items
def get_tcker_type_lst(data_df):
    type_lst = sorted(data_df["type"].unique())
    return type_lst

# get ticker country series: from imported df -called from combine_stock_stats_items
def get_tcker_country_lst(data_df):
    country_lst = sorted(data_df["country"].unique())
    return country_lst

# get ticker exchange series: from imported df -called from combine_stock_stats_items
def get_tcker_exchange_lst(data_df):
    exchange_lst = sorted(data_df["exchange"].unique())
    return exchange_lst

# confirm ifmembers of symbol series exist in symbol list: not finished not returning anything !!!!!!!!!
def filter_tcker_symbollist(symbol_lst):
    if len(symbol_lst) != 0:
        cond_symbol = stocks_df["symbol"].isin(symbol_lst)

# filter tickers stock df for filter conditions
def filter_tcker(apikey_12Data, stocks_df, symbol_select, type_select, country_select, exchange_select):
    lstOfDf = []
    if len(symbol_select) != 0:
        cond_symbol = stocks_df["symbol"].isin(symbol_select)
        df_symbol = stocks_df[cond_symbol]
        lstOfDf.append(df_symbol)
    if len(type_select) != 0:
        cond_type = stocks_df["type"].isin(type_select)
        df_type = stocks_df[cond_type]
        lstOfDf.append(df_type)
    if len(country_select) != 0:
        cond_country = stocks_df["country"].isin(country_select)
        df_country = stocks_df[cond_country]
        lstOfDf.append(df_country)
    if len(exchange_select) != 0:
        cond_exchange = stocks_df["exchange"].isin(exchange_select)
        df_exchange = stocks_df[cond_exchange]
        lstOfDf.append(df_exchange)

    if len(lstOfDf) == 0:
        df_filter = stocks_df
    elif len(lstOfDf) == 1:
        df_filter = lstOfDf[0]
    elif len(lstOfDf) == 2:
        df_filter = pd.merge(lstOfDf[0], lstOfDf[1], how='inner', on=[
                             'symbol', 'type', 'country', 'exchange'], suffixes=('', '_DROPA')).filter(regex='^(?!.*_DROPA)')
    elif len(lstOfDf) == 3:
        df_filter = pd.merge(lstOfDf[0], lstOfDf[1], how='inner', on=[
                             'symbol', 'type', 'country', 'exchange'], suffixes=('', '_DROPA')).filter(regex='^(?!.*_DROPA)')
        df_filter = pd.merge(df_filter, lstOfDf[2], how='inner', on=[
                             'symbol', 'type', 'country', 'exchange'], suffixes=('', '_DROPB')).filter(regex='^(?!.*_DROPB)')
    elif len(lstOfDf) == 4:
        df_filter = pd.merge(lstOfDf[0], lstOfDf[1], how='inner', on=[
                             'symbol', 'type', 'country', 'exchange'], suffixes=('', '_DROPA')).filter(regex='^(?!.*_DROPA)')
        df_filter = pd.merge(df_filter, lstOfDf[2], how='inner', on=[
                             'symbol', 'type', 'country', 'exchange'], suffixes=('', '_DROPB')).filter(regex='^(?!.*_DROPB)')
        df_filter = pd.merge(df_filter, lstOfDf[3], how='inner', on=[
                             'symbol', 'type', 'country', 'exchange'], suffixes=('', '_DROPC')).filter(regex='^(?!.*_DROPC)')
    df_filter, symb_error_out_shre_lst, symb_error_flt_shre_lst = combine_stock_stats_items(
        apikey_12Data, df_filter)
    df_filter = addEarliestTimeStampsSeries(apikey_12Data, df_filter)
    return df_filter, symb_error_out_shre_lst, symb_error_flt_shre_lst

# add time-stamp series to stock dataframe
def addEarliestTimeStampsSeries(apikey_12Data, df_filter):
    str_timestamp_lst = []
    unx_timestamp_lst = []
    for indx in df_filter.index:
        symbol = df_filter['symbol'][indx]
        earliest_dct = getTickerEarliesrTimeStamp(apikey_12Data, symbol)
        earilest_dt_str = earliest_dct['datetime_data']
        earilest_dt_unx = earliest_dct['unix_time_data']
        str_timestamp_lst.append(earilest_dt_str)
        unx_timestamp_lst.append(earilest_dt_unx)
    df_filter["earliest_timestamp"] = str_timestamp_lst
    df_filter["earliest_timestamp_unix"] = unx_timestamp_lst
    return df_filter

#combine stock df with shares float/outstanding series
def combine_stock_stats_items(apikey_12Data, data_df):
    # get listing of symbols
    symbol_lst = get_tcker_symbol_lst(data_df)
    cond_lst = []
    shares_outstand_lst = []
    float_shares_lst = []
    symb_error_out_shre_lst = []
    symb_error_flt_shre_lst = []
    # loop names to get 2 shares data
    for symbol in symbol_lst:
        shares_outstand_data, float_shares_data, error_out_shre, error_flt_shre = get_tck_stats_items_from_yFin(
            symbol)
        # append symbols not returning outstanding/float shares to error lists
        if error_out_shre == True:
            symb_error_out_shre_lst.append(symbol)
        if error_flt_shre == True:
            symb_error_flt_shre_lst.append(symbol)

        cond = (data_df["symbol"] == symbol)

        cond_lst.append(cond)
        shares_outstand_lst.append(shares_outstand_data)
        float_shares_lst.append(float_shares_data)

    data_df["shares-outstanding"] = np.select(cond_lst, shares_outstand_lst)
    data_df["float-shares"] = np.select(cond_lst, float_shares_lst)
    return data_df, symb_error_out_shre_lst, symb_error_flt_shre_lst

    # append data to data_df
    #data_df = get_tck_stocks_df(apikey_12Data)

#get and clean up a list of tickers from a string 
def get_tcker_lst_fromStringIO(string_data):
    lines = string_data.split("\n")
    string = []
    tcker_lst = []
    for line in lines:
        line = line.replace('-\n', '')
        line = line.replace('\r', '')
        line = line.replace(',,', ',')
        line = line.replace(', ', ',')
        string.append(line)
        tckerItemPerLine = line.split(",")
        for tckers in tckerItemPerLine:
            if tckers.startswith("'") and tckers.endswith("'"):
                tckers = tckers[1:-1]
            elif tckers.startswith('"') and tckers.endswith('"'):
                tckers = tckers[1:-1]
            tckers = tckers.upper()
            if tckers != " ":
                if tckers != "":
                    tcker_lst.append(tckers)
    return tcker_lst

#convert datetime object to string of length 10
def convertDateTimeToDateStrLen10(dateTimeObj):
    StringLen10 = dateTimeObj.strftime("%Y-%m-%d")
    return StringLen10

#convert string of length 10 to string of length 19
def convertDateStrLen10toDateStrLen19(StringLen10):
    if len(StringLen10) == 10:
        StringLen19 = f'{StringLen10} 00:00:00'
    else:
        pass
    return StringLen19

#convert string of length 10 to datetime object
def convertDateStrLen10toDateTime(StringLen10):
    StringLen19 = convertDateStrLen10toDateStrLen19(StringLen10)
    datetimeObj = datetime.strptime(StringLen19, "%Y-%m-%d %H:%M:%S")
    return datetimeObj

#convert string of length 10 to datetime object with NoHrsMinSecs
def convertDateStrLen10toDateTimeNoHrsMinSecs(StringLen10):
    datetimeObj = datetime.strptime(StringLen10, "%Y-%m-%d")
    return datetimeObj

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class CatchJsonError(Error):
    """Raised when error code from json object"""
    """Exception raised for errors in the input salary.
    Attributes:
        salary -- input salary which caused the error
        message -- explanation of the error
    """
    def __init__(self, code, message, status):
        self.code = code
        self.message = message
        self.status = message
        super().__init__(self.message)
    def __str__(self):
        st.error(f'code: {code}  \nmessage:{message}  \nstatus: {status}')
        return f'{self.code}  \n{self.message}  \nstatus: {status}'

# WORK IN PROGRESS!!!!!!! check json object for api errors
def chkJsonObj(json_object):
    #get the keys of json object dictr
    keys = json_object.keys()
    #check if error code json object exist in our json object keys
    error_keys = ['code', 'message', 'status']
    
    trueCnt = 0
    falseCnt = 0
    """ trueCnt values above zero tells us the error keys exist as keys of json dict
        falseCnt values above zero tells us at least 1 error keys is not a member key of json dict"""
    for error_key in error_keys:
        testval = error_key in keys
        if testval == True:
            trueCnt += 1
        else:
            falseCnt += 1
    # tells us this is a valid json object and returns it for onward use
    if falseCnt > 0:
       return json_object
    # tells us this json object is an error json thrown out
    else:
        code = json_object['code']
        message = json_object['message']
        status = json_object['status']
        raise CatchJsonError(code, message, status)

        
# def function to get earliest timestamp for each stock ticker needs checking/running!!!!!!
def getTickerEarliesrTimeStamp(twelvedata_api_key, ticker):
    data_types = ["earliest_timestamp"]
    #twelvedata_url = f'https://api.twelvedata.com/{data_types}?symbol={ticker}&interval=1day&apikey={twelvedata_api_key}'
    twelvedata_url = f'https://api.twelvedata.com/earliest_timestamp?symbol={ticker}&interval=1day&apikey={twelvedata_api_key}'
    json_object = requests.get(twelvedata_url).json()
    json_object = chkJsonObj(json_object)
    #session = requests.Session()
    # In case I run into issues, retry my connection
    #retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    #session.mount('http://', HTTPAdapter(max_retries=retries))
    # Initial request to get the ticker count
    #r = session.get(twelvedata_url)
    #json_object = r.json()
   
    datetime_data = json_object['datetime']
    unix_time_data = json_object['unix_time']
    mydict = {}
    mydict['datetime_data'] = datetime_data
    mydict['unix_time_data'] = unix_time_data
    return mydict


# function adds atime interval to a date using relative time delta calculations
def addRelTimeDelta(date_dt, timeIntervalValue, timeIntervalUnit):
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

    #datetime_object = datetime.strptime(date_str,  '%Y-%m-%d %H:%M:%S')
    datetime_object = date_dt
    datetime_object += rel_delta
    new_date_str = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
    new_date_dt = datetime.strptime(new_date_str,  '%Y-%m-%d %H:%M:%S')
    return new_date_dt


""" # returns list of calculated start/end time/date that program will run to get complete range of data: 
    use this to circumspect the 5000entries limit per api call
    """
@st.cache(suppress_st_warning=True) 
def getStartStopRngeLst(symbol, interval, start_date_dt, end_date_dt):
    # required data
    maxRequestPerDay_freekey = 800
    maxNosDataPts = 5000
    useNosDataPts = 4500

    interval_lst = ['1min', '5min', '15min', '30min',
                    '45min', '1h', '2h', '4h', '1day', '1week', '1month']
    intervalQty_lst = [1,  5,  15,  30,  45,
                       60,  120, 240,  1440,  10080,  44640]

    start_date_str = start_date_dt.strftime("%Y-%m-%d %H:%M:%S")
    end_date_str = end_date_dt.strftime("%Y-%m-%d %H:%M:%S")

    # get difference between start and end dates
    #timedelta_raw = parsed_end - parsed_start
    timedelta_raw = end_date_dt - start_date_dt
    timedeltaInSeconds_int = timedelta_raw.total_seconds()
    timedeltaInMinutes_int = timedeltaInSeconds_int / 60

    # dictionary of mins/bar mapped against interval ie 5mins:5
    interval_intervalQty_dict = {
        interval_lst[i]: intervalQty_lst[i] for i in range(len(interval_lst))}
    intervalInMinutes = interval_intervalQty_dict[interval]

    #calculate total nos of datapoints
    data_pts_total = math.ceil(timedeltaInMinutes_int/intervalInMinutes)

    #if data_pts_total <= useNosDataPts:
    #    use_Rnge_per_Request_int      = useNosDataPts * data_pts_total
    #    use_Rnge_per_Request_datetime = timedelta(seconds=(timedeltaInMinutes_int * 60))
    #else:
    #    use_Rnge_per_Request_int      = useNosDataPts * data_pts_total
    #    use_Rnge_per_Request_datetime = timedelta(seconds=(useNosDataPts * intervalInMinutes * 60))


    #calculate the total number of start/stop pairs or requests to make
    nosReq = math.ceil(data_pts_total/useNosDataPts)


    # we are creating lists of start date/enddate/time interval
    symbol_namn_lst = []
    start_time_lst = []
    end_time_lst = []
    interval_lst = []
    intervalinMin_lst = []
    data_pts_lst = []
    chartRnge_lst = []
    
    cnt = 0
    leftOverDatapts = data_pts_total
    for nos in range(nosReq):
        # populate entries
        if nos == 0:
            start_time_entry = start_date_dt
        else:
            start_time_entry = end_time_lst[nos - 1]
        # can switch to max_Rnge_per_Request_int instead of use_Rnge_per_Request_int
        
        interval_entry = intervalInMinutes
        
        if data_pts_total <= useNosDataPts:
            data_pts_entry = data_pts_total
        else:
            data_pts_entry = useNosDataPts
        # can switch to max_Rnge_per_Request_int instead of use_Rnge_per_Request_int
        ChartRnge_entry = data_pts_total
        
        # correct the last data_pts_entry
        #st.write(f'a1 {cnt}: {leftOverDatapts} : {data_pts_total} : {data_pts_entry}')
        if leftOverDatapts >= data_pts_entry:
            leftOverDatapts = leftOverDatapts - data_pts_entry
        else: 
            data_pts_entry = leftOverDatapts
        #st.write(f'a2 {cnt}: {leftOverDatapts} : {data_pts_total} : {data_pts_entry}')

        use_Rnge_per_Request_int = data_pts_entry * intervalInMinutes * 60
        use_Rnge_per_Request_datetime = timedelta(seconds=(use_Rnge_per_Request_int))
        end_time_entry = start_time_entry + use_Rnge_per_Request_datetime

        # populate lists
        start_time_lst.append(start_time_entry)
        end_time_lst.append(end_time_entry)
        interval_lst.append(interval)
        intervalinMin_lst.append(interval_entry)
        data_pts_lst.append(data_pts_entry)
        chartRnge_lst.append(ChartRnge_entry)
        symbol_namn_lst.append(symbol)
        cnt += 1

    # lets create dataframe from lists created above
    chartTSInput_dict = {"symbol": symbol_namn_lst, "start_time": start_time_lst, "end_time": end_time_lst, 
                        "interval": interval_lst, "interval_mins": intervalinMin_lst,
                         "data_pts_limit": data_pts_lst, "data_pts_all": chartRnge_lst}
    chartTSInput_df = pd.DataFrame(chartTSInput_dict)
    st.dataframe(chartTSInput_df)
    return chartTSInput_df, maxRequestPerDay_freekey


#function to get list of time series for each symbol in a list of symbols
def getAllSymbolTimeSeries_dfs(twelvedata_api_key, symbol_startend_dict):
    symbol_list             = symbol_startend_dict["symbol"]
    allSymb_startEnd_lst    = symbol_startend_dict["start_stop_data"]
    
    all_symb_dc_lst = []
    
    msg_all = ''
    
    msg = '*' * 60
    msg_all = msg_all + msg + '  \n'
    
    msg = f'Working on Getting all TimeSeries DataClasses for:'
    msg_all = msg_all + msg + '  \n'

    msg = f'{symbol_list}'
    msg_all = msg_all + msg + '  \n'
 
    msg = f'total nos of start stop dataframes {len(allSymb_startEnd_lst)}'
    msg_all = msg_all + msg + '  \n'
    msg = '*' * 60
    msg_all = msg_all + msg + '  \n'

    st.info(msg_all)

    
    cnt = 0 
    for symb_df in allSymb_startEnd_lst:
        rows = len(symb_df.index)
        msg_all = ''
        msg = f'Working on Getting TimeSeries DataClass for {cnt}: {symbol_list[cnt]}'
        msg_all = msg_all + msg + '  \n'
        msg = f'Number of Start/End Rows: {rows}'
        msg_all = msg_all + msg + '  \n'
        
        symb_uniq_lst = symb_df['symbol'].unique()
        if len(symb_uniq_lst) == 1:
            symbol = symb_uniq_lst[0]
            msg = f'{cnt} :working on {symbol} df'
            msg_all = msg_all + msg + '  \n' 
        else:
            msg = f'problem: more than one symbol in symbol column'
            msg_all = msg_all + msg + '  \n' 
            msg = f'{symb_uniq_lst}'
            msg_all = msg_all + msg + '  \n' 
        
        for indx in symb_df.index:
            msg = f'Ticker: {symbol}|index nos: {indx} | Start Time: {symb_df["start_time"][indx]} | End Time: {symb_df["end_time"][indx]}'
            msg_all = msg_all + msg + '  \n'

        st.warning(msg_all)
        symb_dc = getSymbol_dc(twelvedata_api_key, symb_df)
        all_symb_dc_lst.append(symb_dc)
        cnt += 1
    
    res_dct = {symbol_list[i]: all_symb_dc_lst[i] for i in range(len(symbol_list))}
    return res_dct
        

# function to get time series for each row of a symbol df in a list of symbols        
def getSymbol_dc(twelvedata_api_key, symb_df):        
    cnt = 0
    symb_cnt = len(symb_df['symbol'].unique())

    if symb_cnt == 1:
        symb_tsData_df_lst  = []
        symb_tsMeta_df_lst  = []
        symb_tsError_df_lst = [] 

        for indx in symb_df.index:
            ticker = symb_df['symbol'][indx]
            start_time = symb_df['start_time'][indx]
            end_time = symb_df['end_time'][indx]
            interval = symb_df['interval'][indx]
            data_pts = symb_df['data_pts_limit'][indx]
    
            tries = 0 
            sleepVal = 3
    
            msg_all = ''
            tsData_df, tsMeta_df, tsError_df = get_TS_12Data(twelvedata_api_key, ticker, interval, start_time, end_time, data_pts, tries,   sleepVal, msg_all)
            
            tsDataLen = len(tsData_df.index)
            if tsDataLen != 0:
                symb_tsData_df_lst.append(tsData_df)

            symb_tsMeta_df_lst.append(tsMeta_df)
            
            tsErrorLen = len(tsError_df.index)
            if tsErrorLen != 0:
                symb_tsError_df_lst.append(tsError_df)
        
        tsErrorLstLen = len(symb_tsError_df_lst)
        if tsErrorLstLen == 0:
            cnt = 0 
            testMetaDf = 0
            for df_meta in symb_tsMeta_df_lst:
                if cnt  == 0:
                    compare_df_meta = df_meta
                else:
                    if compare_df_meta.equals(df_meta) != False:
                        testMetaDf = 1
            if testMetaDf == 0:
                df_dc_tsData_all = pd.concat(symb_tsData_df_lst, axis=0)
                #df_dc_tsError_all = pd.DataFrame()
                ticker_dc = populate_ticker_dc(ticker, interval, start_time, end_time, data_pts, compare_df_meta, df_dc_tsData_all)
            else:
                st.error(f'meta df error') 
        else:
            st.error(f'error df error')

            #    
            #timeSeries_dc = get_TimeSeries_12Data(twelvedata_api_key, ticker, interval, start_time, data_pts, tries, sleepVal, msg_all)
        #    st.write(timeSeries_dc)
        #    symb_timeSeries_dc_lst.append(timeSeries_dc)
        #    cnt +=1
        #singleSymb_Combined_dc = combineTimeSeries_dc(symb_timeSeries_dc_lst)
        ## get output of data
        #dc_ticker           = singleSymb_Combined_dc.ticker
        #dc_interval         = singleSymb_Combined_dc.interval
        #dc_start_date       = singleSymb_Combined_dc.start_date
        #dc_outputsize       = singleSymb_Combined_dc.outputsize
        #dc_status_message   = singleSymb_Combined_dc.status_message
        #df_dc_tsMeta        = singleSymb_Combined_dc.df_tsMeta
        #df_dc_tsData        = singleSymb_Combined_dc.df_tsData
        #df_dc_tsError       = singleSymb_Combined_dc.df_tsError
#   
        ## check ticker_dc contents
        #dc_content = []
        #dc_content.append(f'ticker check for {dc_ticker}  \n')
        #dc_content.append(f'ticker interval is {dc_interval}  \n')
        #dc_content.append(f'ticker stock data from date {dc_start_date}  \n')
        #dc_content.append(f'output size/data points {dc_outputsize}  \n')
        #dc_content.append(f'status message {dc_status_message}  \n')
        #dc_content.append(f'column qty of df_tsMeta is {len(df_dc_tsMeta.index)}  \n')
        #dc_content.append(f'column qty of df_tsData is {len(df_dc_tsData.index)}  \n')
        #dc_content.append(f'column qty of df_tsError is {len(df_dc_tsError.index)}  \n')
#   
        ##msg_all = ''
        ##for dc_item in dc_content:
        ##    msg_all = msg_all + dc_item
        ##st.info(msg_all)
        ##print('+' * 60)
        ##print(msg_all)
        ##print('+' * 60)
        ##st.write(len(df_dc_tsData.index))
        ##st.dataframe(df_dc_tsData)
        #return singleSymb_Combined_dc

def get_TS_12Data(twelvedata_api_key, ticker, interval, start_time, end_time, data_pts, tries, sleepVal, msg_all):
    maxtry = 20
    # TwelveData Work
    data_type = "time_series"
    value_type = ["values"]
    
    # initialise empty dataframes
    tsMeta_df = pd.DataFrame()
    tsData_df = pd.DataFrame()
    tsError_df = pd.DataFrame()
    counter = 0

    twelvedata_url = f"https://api.twelvedata.com/{data_type}?symbol={ticker}&start_date={start_time}&end_date={end_time}&interval={interval}&apikey={twelvedata_api_key}"
    
    json_object = requests.get(twelvedata_url).json()
    #json_object = chkJsonObj(json_object)

    # check if status key exists?
    if ('status' in json_object):
        status_exist = True
    else:
       status_exist = False
    if (status_exist == True):
        status_data = json_object['status']
        #check status value says ok before we extract data
        if status_data == 'ok':
            msg = f'Status Key Check Ok!!!: TS Data Extraction Successful  \nstatus_data == ok for ticker: {ticker}|interval {interval}Start time: start_time|output size: {data_pts}'
            msg_all = msg_all + msg + '  \n'
            
            status_mess = status_data
            meta_data = json_object['meta']
            # will add start and end dates to meta_df
            tsMeta_df = pd.DataFrame(meta_data, index=[0])
            value_data = json_object[f'{value_type[counter]}']
            # will add start and end dates to meta_df
            tsData_df = pd.DataFrame(value_data)
            tsData_df = tsData_df.iloc[::-1].reset_index(drop=True)
        elif status_data == 'error':
            code_data = json_object['code']
            if code_data == 429:
                if tries == (maxtry + 1):
                    msg = f'Time Series Data Extraction Failed!!!!  \nstatus_data == error for ticker: {ticker}|interval {interval}Start time: start_time|output size: {data_pts}'
                    msg_all = msg_all + msg + '  \n'
                    status_mess = status_data
                    code_data = json_object['code']
                    mess_data = json_object['message']
                    error_data = json_object
                    error_df = pd.DataFrame(json_object, index=[0])
                    if data_type == "time_series":
                        tsError_df = error_df
                else:
                    status_mess = status_data
                    tries += 1
                    sleepVal += 1 
                    msg = f'Retry TS Data API call for {ticker}|interval {interval}|Start time: {start_time}|End time: {start_time}output size: {data_pts}  \nRetrying for |Times: {tries}|Secs of Sleep: {sleepVal}'
                    msg_all = msg_all + msg + '  \n'
                    if sleepVal > 0:
                        sleep(sleepVal) 
                    st.write(f'fuck this{msg_all}')                  
                    get_TS_12Data(twelvedata_api_key, ticker, interval, start_time, data_pts, tries, sleepVal, msg_all)
            elif code_data == 400:
                message_data = json_object['message']
                st.error(f'error code: {code_data}  \nmessage: {message_data}  \nstatus: {status_data}')
            else:
                message_data = json_object['message']
                st.error(f'error code: {code_data}  \nmessage: {message_data}  \nstatus: {status_data}')
                
    elif (status_exist == False):
        msg = f'Status Key Does not exist!!!: Will attempt TS Data Extraction from odd json object  \nstatus_data not exist for ticker:{ticker}|interval {interval}|Start time: start_time|output size: {data_pts}'
        msg_all = msg_all + msg + '  \n'
        st.write('status_exist == False')
        status_mess = 'status key not exist'
        meta_data = json_object['meta']
        # will add start and end dates to meta_df
        tsMeta_df = pd.DataFrame(meta_data, index=[0])
        value_data = json_object[f'{value_type[counter]}']
        tsData_df = pd.DataFrame(value_data)
        tsData_df = tsData_df.iloc[::-1].reset_index(drop=True)
    TSQty = len(tsData_df.index)
    if len(tsData_df.index) > 0:
        st.info(f'Time Series Data Successfully extracted: {ticker}|{interval}|{start_time}|{end_time}|{data_pts}|{TSQty}')
        st.dataframe(tsData_df)
    
    return tsMeta_df, tsData_df, tsError_df







def combineTimeSeries_dc(symb_timeSeries_dc_lst):
    cnt = 0
    msg_all = ''

    df_dc_tsData_all = pd.DataFrame()
    tsData_df_lst = []
    tsDataLen = 0
    dc_outputsize_all = 0
    Error_chk = 0
    
    if len(symb_timeSeries_dc_lst) > 0:
        pass
    else:
        Error_chk = 1
        msg = f'DataClass List  for Ticker has Zero members'
        msg_all = msg_all + msg + '  \n'    
    
    msg = f'Processing of Ticker Dataclass List starts now'
    msg_all = msg_all + msg + '  \n'    
    for ticker_dc in symb_timeSeries_dc_lst:
        msg = f'dataclass nos.: {cnt}|symbol: {ticker_dc.ticker}|start date: {ticker_dc.start_date}|max data_pts: {ticker_dc.outputsize}|actual data_pts: {len(ticker_dc.df_tsData.index)}'
        msg_all = msg_all + msg + '  \n'
        
        if len(ticker_dc.df_tsError.index) == 0:
            pass
        else:
            Error_chk = 1
            msg = f'invalid dataclass: current dataclass error-df is not zero'
            msg_all = msg_all + msg + '  \n'
        
        if ticker_dc.status_message == 'ok':
            pass
        else:
            Error_chk = 1
            msg = f'invalid dataclass: current dataclass status message is not ok'
            msg_all = msg_all + msg + '  \n'

        if cnt == 0:
            dc_ticker_00           = ticker_dc.ticker
            dc_interval_00         = ticker_dc.interval
            dc_start_date_00       = ticker_dc.start_date
            dc_status_message   = ticker_dc.status_message

            df_dc_tsError       = ticker_dc.df_tsError
            df_dc_tsMeta_00        = ticker_dc.df_tsMeta

            dc_outputsize_all       = dc_outputsize_all + ticker_dc.outputsize
            tsDataLen = tsDataLen + len(ticker_dc.df_tsData)
            tsData_df_lst.append(ticker_dc.df_tsData)
        else:
            if  dc_ticker_00 == ticker_dc.ticker:
                pass
            else:
                Error_chk = 1
                msg = f'invalid dataclass: current dataclass symbol not same as first ticker dataclass symbol'
                msg_all = msg_all + msg + '  \n'


            if dc_interval_00  == ticker_dc.interval:
                pass
            else:
                Error_chk = 1
                msg = f'invalid dataclass: current dataclass interval not same as first ticker dataclass interval'
                msg_all = msg_all + msg + '  \n'

            if df_dc_tsMeta_00.equals(ticker_dc.df_tsMeta):
                pass
            else:
                Error_chk = 1
                msg = f'invalid dataclass: current dataclass MetaData Dataframe not same as first ticker dataclass MetaData Dataframe '
                msg_all = msg_all + msg + '  \n'

            if Error_chk == 0:
                dc_outputsize_all = dc_outputsize_all +ticker_dc.outputsize 
                tsDataLen = tsDataLen + len(ticker_dc.df_tsData)
                tsData_df_lst.append(ticker_dc.df_tsData)
                msg = f'total max data_pts is {dc_outputsize_all}|total actual data_pts is {tsDataLen}'
                msg_all = msg_all + msg + '  \n'
            
        cnt += 1
        if Error_chk == 0:
            
            df_dc_tsData_all = pd.concat(tsData_df_lst, axis=0)
            #df_dc_tsData_all = pd.concat(tsData_df_lst, axis=0).drop_duplicates()

            st.info(msg_all)

        
            final_ticker_dc = populate_ticker_dc(dc_ticker_00, dc_interval_00, dc_start_date_00, dc_outputsize_all, dc_status_message,  df_dc_tsMeta_00, df_dc_tsData_all, df_dc_tsError)
            st.dataframe(df_dc_tsData_all.head(5))
            st.dataframe(df_dc_tsData_all.tail(5))
            return final_ticker_dc
        else:
            st.error(msg_all)
            print('+' * 60)
            print(msg_all)
            print('+' * 60)
        
     

# get stock ticker time series data
# do i need to add timezone?
def get_TimeSeries_12Data(twelvedata_api_key, ticker, interval, start_time, data_pts, tries, sleepVal, msg_all):
    maxtry = 20
    # TwelveData Work
    data_types = ["time_series"]
    value_type = ["values"]
    
    # initialise empty dataframes
    tsMeta_df = pd.DataFrame()
    tsData_df = pd.DataFrame()
    tsError_df = pd.DataFrame()
    counter = 0


    for data_type in data_types:
        # time series data - adjusted close price
        # ref: https://support.twelvedata.com/en/articles/5179064-are-the-prices-adjusted
        twelvedata_url = f"https://api.twelvedata.com/{data_type}?symbol={ticker}&interval={interval}&start_date={start_time}&outputsize={data_pts}&apikey={twelvedata_api_key}"
        #json_object = requests.get(twelvedata_url).json()

        session = requests.Session()
        # In case I run into issues, retry my connection
        retries = Retry(total=5, backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        # Initial request to get the ticker count
        r = session.get(twelvedata_url)
        json_object = r.json()
        json_object = chkJsonObj(json_object)

        #st.json(json_object)

        # check if status key exists?
        error_code = 0
        if ('status' in json_object):
            status_exist = True
            
        else:
           status_exist = False
           error_code = 1

        if (status_exist == True):
            status_data = json_object['status']

            #check status value says ok before we extract data
            if status_data == 'ok':
                msg = f'Status Key Check Ok!!!: TS Data Extraction Successful  \nstatus_data == ok for ticker: {ticker}|interval {interval}|Start time: start_time|output size: {data_pts}'
                msg_all = msg_all + msg + '  \n'
                
                status_mess = status_data
                meta_data = json_object['meta']
                # will add start and end dates to meta_df
                tsMeta_df = pd.DataFrame(meta_data, index=[0])

                value_data = json_object[f'{value_type[counter]}']
                # will add start and end dates to meta_df
                tsData_df = pd.DataFrame(value_data)
                tsData_df = tsData_df.iloc[::-1].reset_index(drop=True)
                st.dataframe(tsData_df)

                ticker_dc = populate_ticker_dc(ticker, interval, start_time, data_pts, status_mess,  tsMeta_df, tsData_df, tsError_df)
                
            elif status_data == 'error':
                if tries == (maxtry + 1):
                    msg = f'Time Series Data Extraction Failed!!!!  \nstatus_data == error for ticker: {ticker}|interval {interval}|Start time: start_time|output size: {data_pts}'
                    msg_all = msg_all + msg + '  \n'

                    status_mess = status_data
                    error_code = 1
                    code_data = json_object['code']
                    mess_data = json_object['message']

                    error_data = json_object
                    error_df = pd.DataFrame(json_object, index=[0])

                    if data_type == "time_series":
                        tsError_df = error_df
                    
                    ticker_dc = populate_ticker_dc(ticker, interval, start_time, data_pts, status_mess,  tsMeta_df, tsData_df, tsError_df)
                else:
                    status_mess = status_data
                    tries += 1
                    sleepVal += 1 
                    msg = f'Retry TS Data API call for {ticker}|interval {interval}|Start time: {start_time}|output size: {data_pts}  \nRetrying for |Times: {tries}|Secs of Sleep: {sleepVal}'
                    msg_all = msg_all + msg + '  \n'
                    
                    if sleepVal > 0:
                        sleep(sleepVal)                   
                    ticker_dc = get_TimeSeries_12Data(twelvedata_api_key, ticker, interval, start_time, data_pts, tries, sleepVal, msg_all)
                    

        elif (status_exist == False):
            msg = f'Status Key Does not exist!!!: Will attempt TS Data Extraction from odd json object  \nstatus_data not exist for ticker: {ticker}|interval {interval}|Start time: start_time|output size: {data_pts}'
            msg_all = msg_all + msg + '  \n'
            st.write('status_exist == False')
            st.json(json_object)
            status_mess = 'status key not exist'
            meta_data = json_object['meta']
            # will add start and end dates to meta_df
            tsMeta_df = pd.DataFrame(meta_data, index=[0])

            value_data = json_object[f'{value_type[counter]}']
            tsData_df = pd.DataFrame(value_data)
            tsData_df = tsData_df.iloc[::-1].reset_index(drop=True)
            st.dataframe(tsData_df)

            ticker_dc =  populate_ticker_dc(ticker, interval, start_time, data_pts, status_mess,  tsMeta_df, tsData_df, tsError_df)

        # get output of data
        dc_ticker           = ticker_dc.ticker
        dc_interval         = ticker_dc.interval
        dc_start_date       = ticker_dc.start_date
        dc_outputsize       = ticker_dc.outputsize
        dc_status_message   = ticker_dc.status_message
        df_dc_tsMeta        = ticker_dc.df_tsMeta
        df_dc_tsData        = ticker_dc.df_tsData
        df_dc_tsError       = ticker_dc.df_tsError

        # check ticker_dc contents
        dc_content = []
        dc_content.append(f'ticker check for {dc_ticker}  \n')
        dc_content.append(f'ticker interval is {dc_interval}  \n')
        dc_content.append(f'ticker stock data from date {dc_start_date}  \n')
        dc_content.append(f'output size/data points {dc_outputsize}  \n')
        dc_content.append(f'status message {dc_status_message}  \n')
        dc_content.append(f'column qty of df_tsMeta is {len(df_dc_tsMeta.index)}  \n')
        dc_content.append(f'column qty of df_tsData is {len(df_dc_tsData.index)}  \n')
        dc_content.append(f'column qty of df_tsError is {len(df_dc_tsError.index)}  \n')

        for dc_item in dc_content:
            msg_all = msg_all + dc_item
 

        # testing to see if we ever get error status after repeated retries
        if dc_status_message == 'error':
            msg = f'status error failure level 1'
            msg_all = msg_all + msg
            #l1_status error failure
        if dc_status_message == 'status key not exist':
            msg = f'status key not exist failure level 1'
            msg_all = msg_all + msg
            #l1_status key not exist failure   

        ts_extract_pass = 'Status Key Check Ok!!!: TS Data Extraction Successful'
        ts_extract_fail = 'Time Series Data Extraction Failed!!!!'  
        ts_extract_odd  = 'Status Key Does not exist!!!'   

        
        #Output Time Series Print out for checks 
        #if ts_extract_pass in msg_all:
        #    st.info(msg_all)
        #elif ts_extract_fail in msg_all:
        #    st.error(msg_all)
        #elif ts_extract_fail in msg_all:
        #    st.warning(msg_all)
#
        #print('+' * 60)
        #print(msg_all)
        #print('+' * 60)

        st.dataframe(tsData_df.head(5))
        st.dataframe(tsData_df.tail(5))
        counter += 1
        return ticker_dc
        
        
    

def populate_ticker_dc(ticker, interval, start_time, end_time, data_pts, compare_df_meta, df_dc_tsData_all):
    ticker_dc = singleTickerData(ticker=ticker,
                                     interval=interval,
                                     start_date=start_time,
                                     end_date=end_time,
                                     outputsize=data_pts,
                                     df_tsMeta=compare_df_meta,
                                     df_tsData=df_dc_tsData_all,
                                     )
    return ticker_dc
