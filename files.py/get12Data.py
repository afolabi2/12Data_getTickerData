import requests, json 
import pandas as pd 
import numpy as np
import pathlib
import streamlit as st
from time import sleep
import getYfData as yfd


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
    #fn = "test.txt" # I don't know what is your fn
    #filepath = p / fn
    #with filepath.open("w", encoding ="utf-8") as f:
        #f.write(data)
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

    #creation of json file for files with status ok
    mypath = pathlib.Path(f'{p}', f'{filename}.json')
    with open(mypath, "w") as outfile:
            json.dump(json_object, outfile, indent=4, sort_keys=True)


#convert json key/pair to df if status key is "ok"
def get_tck_apistocks_json_df(json_object, status_hdr='status', json_key='data'):
    status_hdr_exist = chk_json_key_exists(json_key=status_hdr, json_object=json_object)
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
    statistics_exists = chk_json_key_exists(json_key="statistics", json_object = json_object)
    
    if statistics_exists:
        json_object = json_object["statistics"]
        stock_statistics_exists = chk_json_key_exists(json_key="stock_statistics", json_object = json_object)
        if stock_statistics_exists:
            json_object = json_object["stock_statistics"]
            shares_outstand_data = json_object["shares_outstanding"]
            float_shares_data = json_object["float_shares"]
            return shares_outstand_data, float_shares_data
    else:
        # we wont get data if we dont have a premium 12data subscription, go get data from yfinanace
        shares_outstand_data,float_shares_data = yfd.get_yf_float_outstand_shares(symbol)
        return shares_outstand_data, float_shares_data


def get_tck_stats_items_from_yFin(symbol):
    shares_outstand_data,float_shares_data = yfd.get_yf_float_outstand_shares(symbol)
    return shares_outstand_data, float_shares_data


#@st.cache
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
    
    data_df = get_tck_apistocks_json_df(json_object, status_hdr='status', json_key='data')
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
    print(f'symbol_select:{symbol_select}|type_select:{type_select}|country_select:{country_select}|exchange_select:{exchange_select}|')
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
        df_filter = pd.merge(lstOfDf[0], lstOfDf[1], how ='inner', on =['symbol', 'type', 'country', 'exchange'], suffixes=('', '_DROPA')).filter(regex='^(?!.*_DROPA)')
    elif len(lstOfDf) == 3:
        df_filter = pd.merge(lstOfDf[0], lstOfDf[1], how ='inner', on =['symbol', 'type', 'country', 'exchange'], suffixes=('', '_DROPA')).filter(regex='^(?!.*_DROPA)')
        df_filter = pd.merge( df_filter, lstOfDf[2], how ='inner', on =['symbol', 'type', 'country', 'exchange'], suffixes=('', '_DROPB')).filter(regex='^(?!.*_DROPB)')
    elif len(lstOfDf) == 4:
        df_filter = pd.merge(lstOfDf[0], lstOfDf[1], how ='inner', on =['symbol', 'type', 'country', 'exchange'], suffixes=('', '_DROPA')).filter(regex='^(?!.*_DROPA)')
        df_filter = pd.merge( df_filter, lstOfDf[2], how ='inner', on =['symbol', 'type', 'country', 'exchange'], suffixes=('', '_DROPB')).filter(regex='^(?!.*_DROPB)')
        df_filter = pd.merge(df_filter, lstOfDf[3], how ='inner', on =['symbol', 'type', 'country', 'exchange'], suffixes=('', '_DROPC')).filter(regex='^(?!.*_DROPC)')

    df_filter = combine_stock_stats_items(apikey_12Data, df_filter)
    return df_filter


def combine_stock_stats_items(apikey_12Data, data_df):
    #get listing of symbols
    symbol_lst =  get_tcker_symbol_lst(data_df)
    cond_lst = []
    shares_outstand_lst = []
    float_shares_lst = []

    # loop names to get 2 shares data
    for symbol in symbol_lst:
        shares_outstand_data, float_shares_data = get_tck_stats_items_from_yFin(symbol)
        #st.write(f'symbol: {symbol} | shares_outstand_data:{shares_outstand_data} | float_shares_data: {float_shares_data}')
        
        cond = (data_df["symbol"] == symbol)
        
        cond_lst.append(cond)
        shares_outstand_lst.append(shares_outstand_data)
        float_shares_lst.append(float_shares_data)
    
    data_df["shares-outstanding"] = np.select(cond_lst, shares_outstand_lst)
    data_df["float-shares"] = np.select(cond_lst, float_shares_lst)
    return data_df


    # append data to data_df
    #data_df = get_tck_stocks_df(apikey_12Data)


def get_tcker_lst_fromStringIO(string_data):
    lines = string_data.split("\n")
    string = []
    tcker_lst = []
    for line in lines:
        line = line.replace('-\n','')
        line = line.replace('\r','')
        line = line.replace(',,',',')
        line = line.replace(', ',',')
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