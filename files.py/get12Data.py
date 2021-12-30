import requests, json 
import pandas as pd 
import pathlib
import streamlit as st

# function to create folder(nFolder):
@st.cache
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

def get_tcker_list(apikey_12Data):
    data_type = "stocks"
    apikey = apikey_12Data
    twelvedata_url = f'https://api.twelvedata.com/{data_type}'
    json_object = requests.get(twelvedata_url).json()

    ## create json.files folder if not exist
    #p = str(createfolder('files.json'))
    #print(f'json files will be stored in {p} folder')
    #
    ##creation of json file for files with status ok
    #mypath = pathlib.Path(f'{p}', f'{data_type}.json')
    #with open(mypath, "w") as outfile:
    #        json.dump(json_object, outfile)

    types_stocks = ['EQUITY', 'Common', 'Common Stock', 'American Depositary Receipt', 
    'Real Estate Investment Trust (REIT)', 'Unit', 'GDR', 'Closed-end Fund', 
    'ETF', 'Depositary Receipt', 'Preferred Stock', 'Limited Partnership', 
    'OTHER_SECURITY_TYPE', 'Warrant', 'STRUCTURED_PRODUCT', 'Exchange-traded Note', 
    'Right', 'FUND', 'Trust', 'Index', 'Unit Of Beneficial Interest', 
    'MUTUALFUND', 'New York Registered Shares']
    
    if ('status' in json_object):
        status_exist = True
    else:
        status_exist = False
    
    if (status_exist == True):
        status_data = json_object['status']
        if status_data == 'ok':
            data_data = json_object['data']
            data_df = pd.DataFrame(data_data) # this is not quick enough
            # need to filter using "type" column
            types_stocks_fromapi = data_df.type.unique().tolist()
            # we are using stocks from common stock so
            types_stocks_select = ['Common Stock']
            select_df= data_df[data_df.type.isin(types_stocks_select)]



    else:
        select_df = pd.DataFrame()    
    
    nosRows = len(select_df.index)
    if ( nosRows > 0 ):
        select_df = select_df.sort_values(by='symbol',ascending=True)
        name_lst = select_df["symbol"].tolist()
        return name_lst
    else:
        name_lst = []
        return name_lst



