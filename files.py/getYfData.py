import yfinance as yf
import numpy as np

#==========================
# START FUNCTIONS
#==========================
def get_tcker_Obj(symbol):
    tckerObj = yf.Ticker(symbol)
    print("Ticker Object............DONE")
    return tckerObj

def get_tckerInfo_Obj(symbol):
    tckerObj = yf.Ticker(symbol)
    info = tckerObj.info
    print("Ticker info Object............DONE")
    return info


#==========================
# OUTSTANDING SHARES FUNCTION
#==========================
def get_yf_outstand_shares_fromTckrObj(tckerInfo):
    error_outstand_share = False
    try:
        info_outstand_shares = tckerInfo['sharesOutstanding']
        print(f'success shares outstanding data passed')
    except KeyError:
        info_outstand_shares = np.NaN
        error_outstand_share = True
    else:
        print(f'success shares outstanding data passed')
    return error_outstand_share, info_outstand_shares

def get_yf_outstanding_shares(symbol):
    tcker_info = get_tckerInfo_Obj(symbol)
    tcker_outstand_shares = get_yf_outstand_shares_fromTckrObj(tcker_info)

#==========================
# FLOAT SHARES FUNCTION
#==========================
def get_yf_float_shares_fromTckrObj(tckerInfo):
    error_float_share = False
    try:
        info_float_shares = tckerInfo['floatShares']
    except KeyError:
        info_float_shares = np.NaN
        error_float_share = True
    else:
        print(f'success shares float data passed')
    return error_float_share, info_float_shares


def get_yf_float_shares(symbol):
    tcker_info = get_tckerInfo_Obj(symbol)
    tcker_float_shares = get_yf_float_shares_fromTckrObj(tcker_info)


#==========================
# GET BOTH FLOAT AND OUTSTANDING SHARES FUNCTION
#==========================
def get_yf_float_outstand_shares(symbol):
    print("*" * 60)
    print(f'{symbol} outstanding & float shares data extraction initialized')
    print("*" * 60)
    tcker_info = get_tckerInfo_Obj(symbol)
    error_out_shre, tcker_outstand_shares = get_yf_outstand_shares_fromTckrObj(tcker_info)
    #print(f'outstanding shares error code: {error_out_shre}')
    #print(f'outstanding shares value: {tcker_outstand_shares}')
    error_flt_shre, tcker_float_shares = get_yf_float_shares_fromTckrObj(tcker_info)
    #print(f'float shares error code: {error_flt_shre}')
    #print(f'float shares value: {tcker_float_shares}')
    print(f'data extraction completed for {symbol}')
    return tcker_outstand_shares, tcker_float_shares, error_out_shre, error_flt_shre



