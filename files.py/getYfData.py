import yfinance as yf

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
    info_outstand_shares = tckerInfo['sharesOutstanding']
    #print(info_outstand_shares)
    #print("info_outstanding_shares............DONE")
    return info_outstand_shares

def get_yf_outstanding_shares(symbol):
    tcker_info = get_tckerInfo_Obj(symbol)
    tcker_outstand_shares = get_yf_outstand_shares_fromTckrObj(tcker_info)

#==========================
# FLOAT SHARES FUNCTION
#==========================
def get_yf_float_shares_fromTckrObj(tckerInfo):
    info_float_shares = tckerInfo['floatShares']
    #print(info_float_shares)
    #print("info_float_shares............DONE")
    return info_float_shares

def get_yf_float_shares(symbol):
    tcker_info = get_tckerInfo_Obj(symbol)
    tcker_float_shares = get_yf_float_shares_fromTckrObj(tcker_info)


#==========================
# GET BOTH FLOAT AND OUTSTANDING SHARES FUNCTION
#==========================
def get_yf_float_outstand_shares(symbol):
    tcker_info = get_tckerInfo_Obj(symbol)
    tcker_outstand_shares = get_yf_outstand_shares_fromTckrObj(tcker_info)
    tcker_float_shares = get_yf_float_shares_fromTckrObj(tcker_info)
    return tcker_outstand_shares,tcker_float_shares



