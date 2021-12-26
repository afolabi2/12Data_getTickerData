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
from time import sleep
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
#5 get earliest dates a ticker was registered on exchanges: https://twelvedata.com/docs#earliest-timestamp
#6 confirm with flo if 12data covers satisfactorily all exchanges|all tickers
    #|all crypto exchanges|all crypto pairs|requested required info 



# **********************************************
# inview tasks
# **********************************************


# **********************************************
# done tasks
# **********************************************
#Now pls check whats in the dataclass df's to confirm data is in it
#7 confirm if json files produced overwrite or just appends




# data class to hold each ticker data
@dataclass
class singleTickerData(object):
     ticker: str
     df_tsMeta : pd.core.frame.DataFrame
     df_tsData : pd.core.frame.DataFrame
     df_tsError : pd.core.frame.DataFrame

     df_dvMeta : pd.core.frame.DataFrame
     df_dvData : pd.core.frame.DataFrame
     df_dvError : pd.core.frame.DataFrame

     df_spMeta : pd.core.frame.DataFrame
     df_spData : pd.core.frame.DataFrame
     df_spError : pd.core.frame.DataFrame

@dataclass
class multiTickerData(object):
    listTickerDClass: list
    def populatelist(dcItem):
        listTickerDClass.append(dcItem)

@dataclass
class singleTickerInput(object):
    # api keys
    #alpha_vantage_api_key : str = "FYQD4Z70A1KX5QI9"
    twelvedata_api_key: str = "7940a5c7698545e98f6617f235dd1d5d"
    ticker: str = "AAPL"
    earliestdatetime: str
    earliestUnix_time: str
    interval: str = "1min"
    start_date: str = "2016-01-20"
    end_date: str = ""
    timezone: str = ""   

#def createfolder(nFolder, data):
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

# def function to get earliest timestamp for each stock
def getTickerEarliesrTimeStamp(twelvedata_api_key, ticker, interval):
    data_types = ["earliest_timestamp"]
    twelvedata_url = f'https://api.twelvedata.com/{data_types}?symbol={ticker}&interval={interval}&apikey={twelvedata_api_key}'
    #json_object = requests.get(twelvedata_url).json()
    
    session = requests.Session()
    # In case I run into issues, retry my connection
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    # Initial request to get the ticker count
    r = session.get(twelvedata_url)
    json_object = r.json()

    datetime_data = json_object['datetime']
    unix_time_data = json_object['unix_time']
    

def getdata_12data(twelvedata_api_key, ticker, interval, start_date): #do i need to add timezone?
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
        print("+" * 60) 
        print(f'working on {data_type} now')
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
                #print("")
                print("=" * 60)
                print(f'status: {status_data} for {data_type} of {ticker} ticker')
                print(f'{data_type} data captured from twelvedata api for {ticker} ticker')
                print("=" * 60)

                meta_data = json_object['meta']
                meta_df = pd.DataFrame(meta_data, index=[0]) # will add start and end dates to meta_df

                value_data = json_object[f'{value_type[counter]}']
                value_df = pd.DataFrame(value_data) # will add start and end dates to meta_df

                #print(meta_df.head(5))
                #print("+" * 60)
                # print(value_data)
                #print(value_df.head(5))

                mypath = pathlib.Path(f'{p}', f'{ticker}_{data_type}.json')
                with open(mypath, "w") as outfile:
                    json.dump(json_object, outfile)
                
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
                #print("")
                print("=" * 60)
                print(f'{data_type} data error from twelvedata api for {ticker} stock')
                print(f'error code:{code_data} | message: {mess_data}')
                print("=" * 60)

                

                error_data = json_object
                error_df = pd.DataFrame(json_object, index=[0]) 

                if data_type == "time_series":
                    tsError_df = error_df

                elif data_type == "dividends":
                    dvError_df = error_df
                    
                elif data_type == "splits":
                    spError_df = error_df

                mypath = pathlib.Path(f'{p}', f'{ticker}_{data_type}_error.json')
                with open(mypath, "w") as outfile:
                    json.dump(json_object, outfile)

        elif (status_exist == False):
            #print("")
            print("=" * 60)
            print(f'{data_type} data from twelvedata api for {ticker} stock')
            print("=" * 60)

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

            mypath = pathlib.Path(f'{p}', f'{ticker}_{data_type}.json')
            with open(mypath, "w") as outfile:
                json.dump(json_object, outfile)

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
    print(f'column qty of df_tsMeta is {len(ticker_dc.df_tsMeta.columns)}') 
    print(f'column qty of df_tsData is {len(ticker_dc.df_tsData.columns)}') 
    print(f'column qty of df_tsError is {len(ticker_dc.df_tsError.columns)}') 
    print(f'column qty of df_dvMeta is {len(ticker_dc.df_dvMeta.columns)}') 
    print(f'column qty of df_dvData is {len(ticker_dc.df_dvData.columns)}') 
    print(f'column qty of df_dvError is {len(ticker_dc.df_dvError.columns)}') 
    print(f'column qty of df_spMeta is {len(ticker_dc.df_spMeta.columns)}') 
    print(f'column qty of df_spData is {len(ticker_dc.df_spData.columns)}')   
    print(f'column qty of df_spError is {len(ticker_dc.df_spError.columns)}')    
    print("=" * 80)                                   
    return ticker_dc

def returnTickerLst():
    Tickers = ['brtx','gree','sxtc',
         'VCF','NVEC','CPHC','OVBC','LARK','BOTJ','CHMG','USEG','UG',
         'SYTA','ARTW','VFL','UNB','ALAC','HMNF','WAFU','AEHL','GFED',
         'OPHC','OPNT','WSTG','SGMA','AE','EGF','FMY','INDP','CSPI','IOR',
         'NATH','LLL', 'RMED','GRF','LEDS','DXR','HIHO','MRM','AHPI','DTST',
         'PNBK','NXN','AWX','STRT','ISDR','SMIT','ALTM','NEN','PDEX','UTMD',
         'NWLI','WINA', 'DUOT','NVR','CFFI','ACU','AUBN','ARKR','ESBK','CARV',
         'TAYD','JCTCF','AGIL','PATI','ELSE','FCAP','TRT','PW','UBOH','FFHL',
         'RMBL','HFBL', 'DHIL','PFIN','SBET','WTM','IROQ','LTRPB','HSON','BBLG',
         'AIRT','MSVB','GLBZ','JAN','SAL','SVFD','AINC','KEQU','EMCF','LRFC',
         'PFX','NSYS','EDRY','SZC','SFBC','RAND','CLWT','NSEC','KSPN','GBNY',
         'BCACU','RBCN','ESP','SVT','NCSM','NOM','SNOA','HSDT','UUU','JRJC',
         'TTP','INTG','SRV','SUMR','HIFS','MXC','FEMY','BH','AAMC','MAYS','PNRG',
         'MARPS','IKNX','TSRI','CKX','MTEX','ITIC','MTR','BDL','NDP','RHE','ATRI',
         'MXE','ISIG','WVFC','BHV','LIVE','ACY','CNTX','GYRO','VBFC','DJCO','COHN',
         'SEB','CVR','BRTX','DIT','mitq'
          ]
    return Tickers


def main_run():
    tickerlst = returnTickerLst()
    TickerDCLst = []
    for ticker in tickerlst:
        # api keys
        #alpha_vantage_api_key = "FYQD4Z70A1KX5QI9"
        twelvedata_api_key = "7940a5c7698545e98f6617f235dd1d5d"
        #ticker: str = "AAPL"
        interval = "1min"
        start_date = "2016-01-20"
        end_date = ""
        timezone = ""
        singleTickerDC = singleTickerInput(twelvedata_api_key, ticker, interval, start_date, end_date, timezone )
        TickerDCLst.append(singleTickerDC)
    
    multiTickerDCLst = []
    for tickerdata in TickerDCLst:
        single_ticker_dc = getdata_12data(tickerdata.twelvedata_api_key, tickerdata.ticker, tickerdata.interval, tickerdata.start_date)
        multiTickerDCLst.append(single_ticker_dc)

    multi_ticker_dc = multiTickerData(listTickerDClass = multiTickerDCLst)

    for tick in multi_ticker_dc:
        aa = tick.ticker
        print(aa)

if __name__ == "__main__":
    print ("Executing main Program Now")
    main_run()
else:
    print ("Executed when imported")

# code for quick test
#twelvedata_api_key = "7940a5c7698545e98f6617f235dd1d5d"
#tickers = ["AAPL", "brtx"]
#interval = "1min"
#start_date = "2016-01-20"
#TickDClst = []
#for ticker in tickers:
#    singleTickDC = getdata_12data(twelvedata_api_key, ticker, interval, start_date)
#    TickDClst.append(singleTickDC)
#    sleep(10)
#
#AllTickDC = multiTickerData(TickDClst)