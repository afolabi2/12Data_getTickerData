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
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta, MO
import math

from dataclasses import dataclass
from dataclasses import field
from dataclasses import InitVar

# ====================
# DATACLASS FUNCTIONS
# ====================


@dataclass  # data class to hold single ticker dataclass object
class singleTickerData(object):
    ticker: str
    interval: str
    start_date: str
    earliestdatetime: str
    earliestUnix_time: str
    df_tsMeta: pd.core.frame.DataFrame
    df_tsData: pd.core.frame.DataFrame
    df_tsError: pd.core.frame.DataFrame
    df_dvMeta: pd.core.frame.DataFrame
    df_dvData: pd.core.frame.DataFrame
    df_dvError: pd.core.frame.DataFrame
    df_spMeta: pd.core.frame.DataFrame
    df_spData: pd.core.frame.DataFrame
    df_spError: pd.core.frame.DataFrame


@dataclass  # data class to hold list of ticker dataclass object
class multiTickerData(object):
    listTickerDClass: list

    def populatelist(dcItem):
        listTickerDClass.append(dcItem)


@dataclass  # data class to hold input values for each ticker - mostly useless might remove it
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


def get_tck_stats_items(apikey_12Data, symbol):
    data_type = "statistics"
    apikey = apikey_12Data
    twelvedata_url = f'https://api.twelvedata.com/{data_type}?symbol={symbol}&apikey={apikey}'
    json_object = requests.get(twelvedata_url).json()
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


def get_tck_stats_items_from_yFin(symbol):
    shares_outstand_data, float_shares_data, error_out_shre, error_flt_shre = yfd.get_yf_float_outstand_shares(
        symbol)
    return shares_outstand_data, float_shares_data, error_out_shre, error_flt_shre


# @st.cache
def get_tck_stocks_df(apikey_12Data):
    data_type = "stocks"
    apikey = apikey_12Data
    twelvedata_url = f'https://api.twelvedata.com/{data_type}'
    json_object = requests.get(twelvedata_url).json()

    types_stocks = ['EQUITY', 'Common', 'Common Stock', 'American Depositary Receipt',
                    'Real Estate Investment Trust (REIT)', 'Unit', 'GDR', 'Closed-end Fund',
                    'ETF', 'Depositary Receipt', 'Preferred Stock', 'Limited Partnership',
                    'OTHER_SECURITY_TYPE', 'Warrant', 'STRUCTURED_PRODUCT', 'Exchange-traded Note',
                    'Right', 'FUND', 'Trust', 'Index', 'Unit Of Beneficial Interest',
                    'MUTUALFUND', 'New York Registered Shares']

    data_df = get_tck_apistocks_json_df(
        json_object, status_hdr='status', json_key='data')
    return data_df


def get_tcker_symbol_lst(data_df):
    symbol_lst = sorted(data_df["symbol"].unique())
    return symbol_lst


def get_tcker_type_lst(data_df):
    type_lst = sorted(data_df["type"].unique())
    return type_lst


def get_tcker_country_lst(data_df):
    country_lst = sorted(data_df["country"].unique())
    return country_lst


def get_tcker_exchange_lst(data_df):
    exchange_lst = sorted(data_df["exchange"].unique())
    return exchange_lst


def filter_tcker_symbollist(symbol_lst):
    if len(symbol_lst) != 0:
        cond_symbol = stocks_df["symbol"].isin(symbol_lst)


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
    return df_filter, symb_error_out_shre_lst, symb_error_flt_shre_lst


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

def convertDateTimeToDateStrLen10(dateTimeObj):
    StringLen10 = dateTimeObj.strftime("%Y-%m-%d")
    return StringLen10

def convertDateStrLen10toDateStrLen19(StringLen10):
    if len(StringLen10) == 10:
        StringLen19 = f'{StringLen10} 00:00:00'
    else:
        pass
    return StringLen19

def convertDateStrLen10toDateTime(StringLen10):
    StringLen19 = convertDateStrLen10toDateStrLen19(StringLen10)
    datetimeObj = datetime.strptime(StringLen19, "%Y-%m-%d %H:%M:%S")
    return datetimeObj

def convertDateStrLen10toDateTimeNoHrsMinSecs(StringLen10):
    datetimeObj = datetime.strptime(StringLen10, "%Y-%m-%d")
    return datetimeObj


# def function to get earliest timestamp for each stock ticker
def getTickerEarliesrTimeStamp(twelvedata_api_key, ticker, interval):
    data_types = ["earliest_timestamp"]
    #twelvedata_url = f'https://api.twelvedata.com/{data_types}?symbol={ticker}&interval=1day&apikey={twelvedata_api_key}'
    twelvedata_url = f'https://api.twelvedata.com/earliest_timestamp?symbol={ticker}&interval=1day&apikey={twelvedata_api_key}'
    json_object = requests.get(twelvedata_url).json()

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

@st.cache
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
    # if len(start_date) == 10:
    #     start_date = f'{start_date} 00:00:00'
    # if len(end_date) == 10:
    #     end_date = f'{end_date} 00:00:00'
    #parsed_start = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
    #parsed_end = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")

    # get difference between start and end dates
    #timedelta_raw = parsed_end - parsed_start
    timedelta_raw = end_date_dt - start_date_dt
    timedeltaInSeconds_int = timedelta_raw.total_seconds()
    timedeltaInMinutes_int = timedeltaInSeconds_int / 60

    # dictionary of mins/bar mapped against interval ie 5mins:5
    interval_intervalQty_dict = {
        interval_lst[i]: intervalQty_lst[i] for i in range(len(interval_lst))}
    intervalInMinutes = interval_intervalQty_dict[interval]

    # Time Range covered by useNosDataPts and Chart Interval in ints
    use_Rnge_per_Request_int = intervalInMinutes * useNosDataPts
    max_Rnge_per_Request_int = intervalInMinutes * maxNosDataPts

    # Time Range covered by useNosDataPts and Chart Interval in timedelta's
    use_Rnge_per_Request_datetime = timedelta(
        seconds=use_Rnge_per_Request_int * 60)
    max_Rnge_per_Request_datetime = timedelta(
        seconds=max_Rnge_per_Request_int * 60)

    # Nos of Requests to make
    useNosOfRequests = timedeltaInMinutes_int / use_Rnge_per_Request_int
    minNosOfRequests = timedeltaInMinutes_int / max_Rnge_per_Request_int

    useNosOfRequests = math.ceil(useNosOfRequests)
    minNosOfRequests = math.ceil(minNosOfRequests)

    # we need to check that useNosOfRequests, minNosOfRequests are less than maxRequestPerDay_freekey
    # not done yet

    # we are creating lists of start date/enddate/time interval
    symbol_namn_lst = []
    start_time_lst = []
    end_time_lst = []
    interval_lst = []
    intervalinMin_lst = []
    data_pts_lst = []
    chartRnge_lst = []
    for nos in range(useNosOfRequests):
        # populate entries
        if nos == 0:
            start_time_entry = start_date_dt
        else:
            start_time_entry = end_time_lst[nos - 1]
        # can switch to max_Rnge_per_Request_int instead of use_Rnge_per_Request_int
        end_time_entry = start_time_entry + use_Rnge_per_Request_datetime
        interval_entry = intervalInMinutes
        data_pts_entry = useNosDataPts
        # can switch to max_Rnge_per_Request_int instead of use_Rnge_per_Request_int
        ChartRnge_entry = use_Rnge_per_Request_int

        # populate lists
        start_time_lst.append(start_time_entry)
        end_time_lst.append(end_time_entry)
        interval_lst.append(interval)
        intervalinMin_lst.append(interval_entry)
        data_pts_lst.append(data_pts_entry)
        chartRnge_lst.append(ChartRnge_entry)
        symbol_namn_lst.append(symbol)

    # lets create dataframe from lists created above
    chartTSInput_dict = {"symbol": symbol_namn_lst, "start_time": start_time_lst, "end_time": end_time_lst, 
                        "interval": interval_lst, "interval_mins": intervalinMin_lst,
                         "data_pts": data_pts_lst, "chart_Rnge": chartRnge_lst}
    chartTSInput_df = pd.DataFrame(chartTSInput_dict)
    return chartTSInput_df, maxRequestPerDay_freekey


# WORK IN PROGRESS!!!!!!! function to get time series for each row of a symbol df in a list of symbols
#@st.cache
def getAllSymbolTimeSeries_dfs(twelvedata_api_key, allSymb_startEnd_lst):
    df_qty = len(allSymb_startEnd_lst)
    st.write(f"{df_qty} is nos of df's")
    for symb_df in allSymb_startEnd_lst:
        symb_uniq_lst = symb_df['symbol'].unique()
        if len(symb_uniq_lst) == 1:
            symbol = symb_uniq_lst[0]
            st.write(f'working on {symbol} df')
        else:
            st.write(f'problem: more than one symbol in symbol column')
            st.write(f'{symb_uniq_lst}')
        cnt = 0
        timeSeries_lst = []
        for indx in symb_df.index:
            st.write(f'df: {symbol}|row: {indx}:{cnt}')
            ticker = symb_df['symbol'][indx]
            start_time = symb_df['start_time'][indx]
            end_time = symb_df['end_time'][indx]
            interval = symb_df['interval'][indx]
            data_pts = symb_df['data_pts'][indx]
            # plug data to produce a json
            #dc_symbol = 
            timeSeries_df = get_TimeSeries_12Data(twelvedata_api_key, ticker, interval, start_time)
            sleep(5)
            cnt +=1
            # if we dont get desired json files after checks, it should add an error column and error in indx position
            # we need to concatenate all single row entries from each symbol_df and check for duplicate values


# get stock ticker time series data
# do i need to add timezone?
def get_TimeSeries_12Data(twelvedata_api_key, ticker, interval, start_time):
    # TwelveData Work
    data_types = ["time_series"]
    value_type = ["values"]

    counter = 0
    # initialise empty dataframes
    tsMeta_df = pd.DataFrame()
    tsData_df = pd.DataFrame()
    tsError_df = pd.DataFrame()

    for data_type in data_types:
        # time series data - adjusted close price
        # ref: https://support.twelvedata.com/en/articles/5179064-are-the-prices-adjusted
        twelvedata_url = f"https://api.twelvedata.com/{data_type}?symbol={ticker}&interval={interval}&start_date={start_time}&apikey={twelvedata_api_key}"
        #json_object = requests.get(twelvedata_url).json()

        session = requests.Session()
        # In case I run into issues, retry my connection
        retries = Retry(total=5, backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        # Initial request to get the ticker count
        r = session.get(twelvedata_url)
        json_object = r.json()

        #st.json(json_object)

        # check if status key exists?
        if ('status' in json_object):
            status_exist = True
        else:
           status_exist = False

        if (status_exist == True):
            status_data = json_object['status']

            #check status value says ok before we extract data
            if status_data == 'ok':
                meta_data = json_object['meta']
                # will add start and end dates to meta_df
                meta_df = pd.DataFrame(meta_data, index=[0])

                value_data = json_object[f'{value_type[counter]}']
                # will add start and end dates to meta_df
                value_df = pd.DataFrame(value_data)

                if data_type == "time_series":
                    tsMeta_df = meta_df
                    tsData_df = value_df

            #when status value returns error we add an error df? is that not an overkill 
            #we should add that value error to the request df for approprait row
            elif status_data == 'error':
                code_data = json_object['code']
                mess_data = json_object['message']

                error_data = json_object
                error_df = pd.DataFrame(json_object, index=[0])

                if data_type == "time_series":
                    tsError_df = error_df

        elif (status_exist == False):
            meta_data = json_object['meta']
            # will add start and end dates to meta_df
            meta_df = pd.DataFrame(meta_data, index=[0])

            value_data = json_object[f'{value_type[counter]}']
            value_df = pd.DataFrame(value_data)

            if data_type == "time_series":
                tsMeta_df = meta_df
                tsData_df = value_df

        #counter += 1
        #ticker_dc = singleTickerData(ticker=ticker,
        #                             interval=interval,
        #                             start_date=start_date,
        #                             earliestdatetime=earliestDateTime_data,
        #                             earliestUnix_time=earliestUnixTime_data,
        #                             df_tsMeta=tsMeta_df,
        #                             df_tsData=tsData_df,
        #                             df_tsError=tsError_df,
        #                             df_dvMeta=dvMeta_df,
        #                             df_dvData=dvData_df,
        #                             df_dvError=dvError_df,
        #                             df_spMeta=spMeta_df,
        #                             df_spData=spData_df,
        #                             df_spError=spError_df
        #                             )
    ## check ticker_dc contents
    #print("=" * 80)
    #print(f'ticker check for {ticker_dc.ticker}')
    #print(f'ticker interval is {ticker_dc.interval}')
    #print(f'ticker stock data from date {ticker_dc.start_date}')
    #print(
    #    f'Earliest Date-time for {ticker_dc.ticker} is {ticker_dc.earliestdatetime}')
    #print(
    #    f'Earliest Unix-time for {ticker_dc.ticker} is {ticker_dc.earliestUnix_time}')
    #print(f'column qty of df_tsMeta is {len(ticker_dc.df_tsMeta.index)}')
    #print(f'column qty of df_tsData is {len(ticker_dc.df_tsData.index)}')
    #print(f'column qty of df_tsError is {len(ticker_dc.df_tsError.index)}')
    #print(f'column qty of df_dvMeta is {len(ticker_dc.df_dvMeta.index)}')
    #print(f'column qty of df_dvData is {len(ticker_dc.df_dvData.index)}')
    #print(f'column qty of df_dvError is {len(ticker_dc.df_dvError.index)}')
    #print(f'column qty of df_spMeta is {len(ticker_dc.df_spMeta.index)}')
    #print(f'column qty of df_spData is {len(ticker_dc.df_spData.index)}')
    #print(f'column qty of df_spError is {len(ticker_dc.df_spError.index)}')
    #print("=" * 80)
    #return ticker_dc
