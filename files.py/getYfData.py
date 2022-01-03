import yfinance as yf
import numpy as np

#==========================
# START FUNCTIONS
#==========================
def get_tcker_Obj(symbol):
    tckerObj = yf.Ticker(symbol)
    #print("Ticker Object............DONE")
    return tckerObj

def get_tckerInfo_Obj(symbol):
    tckerObj = yf.Ticker(symbol)
    info = tckerObj.info
    #print("Ticker info Object............DONE")
    return info


#==========================
# OUTSTANDING SHARES FUNCTION
#==========================
def get_yf_outstand_shares_fromTckrObj(tckerInfo):
    error_outstand_share = False
    try:
        info_outstand_shares = tckerInfo['sharesOutstanding']
    except KeyError:
        info_outstand_shares = np.NaN
        error_outstand_share = True
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
    return error_float_share, info_float_shares


def get_yf_float_shares(symbol):
    tcker_info = get_tckerInfo_Obj(symbol)
    tcker_float_shares = get_yf_float_shares_fromTckrObj(tcker_info)


#==========================
# GET BOTH FLOAT AND OUTSTANDING SHARES FUNCTION
#==========================
def get_yf_float_outstand_shares(symbol):
    tcker_info = get_tckerInfo_Obj(symbol)
    error_out_shre, tcker_outstand_shares = get_yf_outstand_shares_fromTckrObj(tcker_info)
    error_flt_shre, tcker_float_shares = get_yf_float_shares_fromTckrObj(tcker_info)
    return tcker_outstand_shares, tcker_float_shares, error_out_shre, error_flt_shre



