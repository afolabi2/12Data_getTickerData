import streamlit as st
import pandas as pd

# programmatic calculations
import get12Data as g12d
import getAnalytics as gAna

# gui helper functions
import guiMarkDown as guiMrk #used for markdown and write functions

def initSessionStates():
    # session objects of dataframe type
    if "df_filter" not in st.session_state: 
        st.session_state.df_filter = pd.DataFrame()
    
    # session objects of list type containing dataframe 
    if "lst_df_gui02" not in st.session_state: 
        st.session_state.lst_df_gui02 = [] 
    if "lst_df_gui03" not in st.session_state: 
        st.session_state.lst_df_gui03 = [] 

    if "lst_df_trans" not in st.session_state: 
        st.session_state.lst_df_trans = []
    if "lst_df_Rnge" not in st.session_state: 
        st.session_state.lst_df_Rnge = []
    if "lst_df_Voltle" not in st.session_state: 
        st.session_state.lst_df_Voltle = []
        
    # session objects of list type containing dataframe
    if "lst_Err_OutShr" not in st.session_state: 
        st.session_state.lst_Err_OutShr = []
    if "lst_Err_FltShr" not in st.session_state: 
        st.session_state.lst_Err_FltShr = []

    # session objects of dict type
    if "sess02_dict" not in st.session_state:
        st.session_state.sess02_dict = []
    if "res_dct" not in st.session_state: 
        st.session_state.res_dct = []      

    # session objects of expander type
    if "gui01_expander" not in st.session_state: 
        st.session_state.gui01_expander = st.delta_generator.DeltaGenerator  
    if "gui02_expander" not in st.session_state: 
        st.session_state.gui02_expander = st.delta_generator.DeltaGenerator  
    if "gui03_expander" not in st.session_state: 
        st.session_state.gui03_expander = st.delta_generator.DeltaGenerator  
    if "gui04_expander" not in st.session_state: 
        st.session_state.gui04_expander = st.delta_generator.DeltaGenerator 

# ====================
# HELPER FUNCTIONS
# ====================
def setFilterResult():
        df_filter, lst_Err_OutShr, lst_Err_FltShr = g12d.filter_tcker(st.session_state.Data12_PaidKey, 
                                                            st.session_state.df_stock, st.session_state.symbol_select, 
                                                            st.session_state.type_select, st.session_state.country_select, 
                                                            st.session_state.exchange_select)
        return df_filter, lst_Err_OutShr, lst_Err_FltShr

def getStartEndDates(symbol):
        if (st.session_state.startTimeRangeOption == 'earliestTimeStamp'):
            date_info = g12d.getTickerEarliesrTimeStamp(apikey_12Data, symbol)
            final_start_date_str = date_info['datetime_data']
            final_start_date = g12d.convertDateStrLen10toDateTime(final_start_date_str)         
            
        if (st.session_state.startTimeRangeOption == 'user provided StartDate'):
            final_start_date_str = g12d.convertDateTimeToDateStrLen10(st.session_state.start_date_input)
            final_start_date =  g12d.convertDateStrLen10toDateTime(final_start_date_str)
        
        if (st.session_state.startTimeRangeOption == "Today's Date"):
            final_start_date_str = g12d.convertDateTimeToDateStrLen10(today_date_input)
            final_start_date = g12d.convertDateStrLen10toDateTime(final_start_date_str)          
            
        if (st.session_state.endTimeRangeOption == 'user provided EndDate'):
            final_end_date_str = g12d.convertDateTimeToDateStrLen10(st.session_state.end_date_input)
            final_end_date = g12d.convertDateStrLen10toDateTime(final_end_date_str)          
            
        if (st.session_state.endTimeRangeOption == "Time Interval"):
            final_end_date = g12d.addRelTimeDelta(final_start_date, timeIntervalValue, timeIntervalUnit)
            final_end_date_str = g12d.convertDateTimeToDateStrLen10(final_end_date)
        if (st.session_state.endTimeRangeOption == "Today's Date"):
            final_end_date_str = g12d.convertDateTimeToDateStrLen10(today_date_input)
            final_end_date = g12d.convertDateStrLen10toDateTime(final_end_date_str)
        
        return final_start_date, final_end_date
        
def getSessDict_gui02():
    if len(st.session_state.symbol_select) == 0:
                st.warning('Please populate ticker symbol')
    else:
        lst_fin_start_dte = []
        lst_fin_end_dte = []
        st.session_state.lst_df_gui02 = []
        lst_maxReqDly_freekey = []
        lst_nosOfLoopsPerSymb = []
        
        
        for symbol in st.session_state.symbol_select:
            final_start_date, final_end_date = getStartEndDates(symbol)           
            lst_fin_start_dte.append(final_start_date)
            lst_fin_end_dte.append(final_end_date)
            
            symb_startEnd_df,maxRequestPerDay_freekey = g12d.getStartStopRngeLst(symbol, st.session_state.interval, final_start_date, final_end_date) 
            st.session_state.lst_df_gui02.append(symb_startEnd_df)
            lst_maxReqDly_freekey.append(maxRequestPerDay_freekey)
            
            nosOfLoopsPerSymb = len(symb_startEnd_df.index)
            lst_nosOfLoopsPerSymb.append(nosOfLoopsPerSymb)
        
        sess02_dict = dict()
        sess02_dict["Symbol"]           = st.session_state.symbol_select
        sess02_dict["Start Date"]       = lst_fin_start_dte
        sess02_dict["End Date"]         = lst_fin_end_dte
        sess02_dict["Max FreeKey Req"]  = lst_maxReqDly_freekey
        sess02_dict["Nos of Loops"]     = lst_nosOfLoopsPerSymb
        sess02_dict["df_gui02"]         = st.session_state.lst_df_gui02
        
        return sess02_dict
        

def printGui01(lst_Err_OutShr, lst_Err_FltShr ):
    msg_get12Data = ''
    if len(lst_Err_OutShr) > 0:
        msg = f'outstanding shares data unavailable for {len(lst_Err_OutShr)} Nos. of Tickers'
        msg_get12Data = msg_get12Data + msg + '<br/>'
        msg = lst_Err_OutShr
        msg_get12Data = msg_get12Data + msg + '<br/>'
    if len(lst_Err_FltShr) > 0:
        msg = f'floating shares data unavailable for {len(lst_Err_FltShr)} Nos. of Tickers'
        msg_get12Data = msg_get12Data + msg + '<br/>'
        msg = lst_Err_FltShr
        msg_get12Data = msg_get12Data + msg + '<br/>'
    msg = f"Nos. of Legal tickers: {len(st.session_state.symbol_select)}"
    msg_get12Data = msg_get12Data + msg + '<br/>'
    msg = f'Ticker List: **{st.session_state.symbol_select}'
    msg_get12Data = msg_get12Data + msg + '<br/>'

    with st.session_state.gui01_expander:
        msg = 'Tickers Available from 12Data'
        guiMrk.colorHeader(fontcolor = '#800080', fontsze = 18, msg = msg)
        guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = msg_get12Data)

        if len(st.session_state.df_filter) > 0: 
            msg = 'DataFrame for Filtered Ticker List'
            guiMrk.colorHeader(fontcolor = '#800080', fontsze = 18, msg = msg)
            st.dataframe(st.session_state.df_filter)

def printGui02():
    sess02_dict = st.session_state.sess02_dict
    symbol_select = sess02_dict["Symbol"] # could usest.session_state.symbol_select instead
    lst_nosOfLoopsPerSymb = sess02_dict["Nos of Loops"]
    lst_maxReqDly_freekey = sess02_dict["Max FreeKey Req"]  
    allSymb_startEnd_lst  = sess02_dict["df_gui02"] 
    
    if len(symbol_select) == 0:
                st.warning('Please populate ticker symbol')
    else:
        msg_gui02 = ''
        cnt = 0
        for symbol in symbol_select:
            nosOfLoopsPerSymb = lst_nosOfLoopsPerSymb[cnt] 
            maxRequestPerDay_freekey = lst_maxReqDly_freekey[cnt]
            
            if nosOfLoopsPerSymb > maxRequestPerDay_freekey:
                msg = f'{nosOfLoopsPerSymb} Required Time Series Requests exceeds Daily Free API Limit of {maxRequestPerDay_freekey} Requests for {symbol}'
                msg_gui02 = msg_gui02 + msg + '<br/>'
            else:
                msg = f'{nosOfLoopsPerSymb} Required Time Series Requests wont exceed Daily Free API Limit of {maxRequestPerDay_freekey} Requests for {symbol}'
                msg_gui02 = msg_gui02 + msg + '<br/>'
            cnt += 1

    #get number of tickers to be used
    nosOfTickers = len(allSymb_startEnd_lst)
    msg = f'Nos of Ticker Symbol(s) to process: {nosOfTickers}' + '<br/>'
    msg_gui02 = msg + msg_gui02

    return msg_gui02
    
# ====================
# MAIN LOGIC CALCULATIONS
# ====================        
def mainLogic():
    if st.session_state.button_submit:
        initSessionStates()
        
        #computations for Gui01 here
        df_filter, lst_Err_OutShr, lst_Err_FltShr = setFilterResult()
        st.session_state.df_filter = pd.DataFrame()
        st.session_state.lst_Err_OutShr = []
        st.session_state.lst_Err_FltShr = []
        st.session_state.df_filter = df_filter
        st.session_state.lst_Err_OutShr = lst_Err_OutShr
        st.session_state.lst_Err_FltShr = lst_Err_FltShr
        
        #computations for Gui02 here
        sess02_dict = getSessDict_gui02()
        st.session_state.sess02_dict = sess02_dict
        
        allSymb_startEnd_lst = st.session_state.lst_df_gui02
        symbol_select = st.session_state.symbol_select
        symbol_startend_dict = {"symbol":symbol_select, "start_stop_data": allSymb_startEnd_lst}
        res_dct = g12d.getAllSymbolTimeSeries_dfs(st.session_state.Data12_PaidKey, symbol_startend_dict)
        st.session_state.res_dct = res_dct
        # add value df to session state
        st.session_state.lst_df_gui03 = []
        st.session_state.lst_df_trans = []
        st.session_state.lst_df_Rnge  = []
        st.session_state.lst_df_Voltle  = []
        for key, value in st.session_state.res_dct.items():
            st.session_state.lst_df_gui03.append(value.df_tsData)
            df_trans = gAna.analytics(value.df_tsData)
            st.session_state.lst_df_trans.append(df_trans)
            st.session_state.lst_df_Rnge.append(gAna.df_filter_Range(df_trans))

        
    mess = f"We are done.....Success!!!!<br/>see results below"
    guiMrk.colorHeader(fontcolor = '#800080', fontsze = 15, msg = mess) 
    #we need to create a testing of expected values to confirm proper success
# ====================
# MAIN AREA GUI'S
# ====================
def guiLoad():
    #create main area gui
    gui01()
    gui02()
    gui03()
    gui04()


def gui01():
    #initialize session states to be used
    initSessionStates()
    
    st.session_state.gui01_expander = st.expander(f"12Data Tickerlist Dataframe containing Outstanding & Float Shares")
    st.sidebar.markdown("---")
    
    lst_Err_OutShr = st.session_state.lst_Err_OutShr 
    lst_Err_FltShr = st.session_state.lst_Err_FltShr
    printGui01(lst_Err_OutShr, lst_Err_FltShr )

def gui02():
    initSessionStates()
    st.session_state.gui02_expander = st.expander(f"12Data Input for Time Series Computations")            
    msg_gui02 = printGui02()
    # writing of data    
    with st.session_state.gui02_expander:
        mess = f'Ticker Dataframes for Start Stop Date Ranges'
        guiMrk.colorHeader(fontcolor = '#800080', fontsze = 20, msg = mess)
        guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = msg_gui02)

        cnt = 0
        len1 = len(st.session_state.lst_df_gui02)
        len2 = len(st.session_state.symbol_select)
        for dataframe in st.session_state.lst_df_gui02:
            symbol_select = st.session_state.symbol_select
            symbol = symbol_select[cnt]
            st.write('*' * 60)
            mess = f'{symbol} Requests Start Stop Date Range DataFrame'
            guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = mess)
            st.dataframe(dataframe)
            cnt+=1
        st.write('*' * 60)

def gui03():
    st.session_state.gui03_expander = st.expander(f"12Data Output for Time Series Computations")        
    with st.session_state.gui03_expander:
        for key, value in st.session_state.res_dct.items():
            msg_gui03 = ''
            total_data_pts = len(value.df_tsData.index)
            msg = f'{value.ticker} Available Time Series Dataframe between {value.start_date} and {value.end_date}'
            msg_gui03 = msg_gui03 + msg + '<br/>'

            msg = f'{value.ticker} has Max Nos of DataPoints:{value.outputsize}'
            msg_gui03 = msg_gui03 + msg + '<br/>'
            msg = f'{value.ticker} has Total DataPoints:{total_data_pts}'
            msg_gui03 = msg_gui03 + msg + '<br/>'

            # writing of data
            mess = f'{value.ticker}: Ticker Dataframes for Time Series Data'
            guiMrk.colorHeader(fontcolor = '#800080', fontsze = 20, msg = mess)            
            guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = msg_gui03)

            #st.dataframe(df_gui03)
            st.dataframe(value.df_tsData)

# gui04 needs to be seperated from logic
def gui04():
    st.session_state.gui04_expander = st.expander(f"Analytics for Time Series Computations")
    with st.session_state.gui04_expander:
        mess = f'Ticker Dataframes for Analytics'
        guiMrk.colorHeader(fontcolor = '#800080', fontsze = 20, msg = mess)
        cnt = 0
        for key, value in st.session_state.res_dct.items():
            df_trans = st.session_state.lst_df_trans[cnt]
            
            if len(df_trans.index) > 0:
                minMaxform = st.form(f"MinMax_Volatile_Column_{cnt}")
                placeholder = st.empty()
                with minMaxform:
                    RangeMin, RangeMax = gAna.df_getMinMaxVal_Volatile(df_trans)
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        entry = ''
                        entry_ = f"Filter by Volatile Column "
                        entry  = entry + entry_ + '<br/>'
                        entry_ = f'min value: {RangeMin} <br/> max value {RangeMax}'
                        entry = entry + entry_ + '<br/>'
                        guiMrk.colorHeader(fontcolor = '#008000', fontsze = 18, msg = entry)
                    with col2:
                        volatile_slide = st.slider('Min and Max Volatile Column Range?', value = [RangeMin, RangeMax])
                    submit_button = st.form_submit_button(label='Submit')
                    
                if submit_button:
                    minVal = volatile_slide[0]
                    maxVal = volatile_slide[1]
                    df_Voltle = gAna.df_filter_Volatile(df_trans, minVal, maxVal)
                    st.session_state.lst_df_Voltle.append(df_Voltle)
                    if len(df_Voltle.index) > 0:
                        volrange = len(df_Voltle.index)
                        msg_gui04 = ''
                        msg = f'Data Analytic Dataframe for :{value.ticker}'
                        msg_gui04 = msg_gui04 + msg + '<br/>'
                        msg = f'filtered by Volatile Column'
                        msg_gui04 = msg_gui04 + msg + '<br/>'
                        msg = f'filtered Volatile Dataframe of {volrange} Rows of {len(df_trans.index)}'
                        msg_gui04 = msg_gui04 + msg + '<br/>'
                        msg = f'Volatile column values range between {minVal} - {maxVal}'
                        msg_gui04 = msg_gui04 + msg + '<br/>'
                        
                    else:
                        msg_gui04 = ''
                        msg = f'No Volatile Dataframe for :{value.ticker}'
                        msg_gui04 = msg_gui04 + msg + '<br/>'
                   
                    with placeholder.container():
                        guiMrk.colorHeader(fontcolor = '#FF0000', fontsze = 14, msg = msg_gui04)
                        st.dataframe(st.session_state.Voltle_df)
                else:
                    with placeholder.container():
                        msg_gui04 = ''
                        msg = f'Data Analytic Dataframe for :{value.ticker}'
                        msg_gui04 = msg_gui04 + msg + '<br/>'
                        msg = f'No Filters applied'
                        msg_gui04 = msg_gui04 + msg + '<br/>'
                        guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = msg_gui04)
                        st.dataframe(st.session_state.trans_df)
                    
                df_Rnge = st.session_state.lst_df_Rnge[cnt]
                if len(df_Rnge.index) > 0:
                    msg_gui04 = ''
                    msg = f'Data Analytic Dataframe for :{value.ticker}'
                    msg_gui04 = msg_gui04 + msg + '<br/>'
                    msg = f'filtered by Range Column'
                    msg_gui04 = msg_gui04 + msg + '<br/>'
                    guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = msg_gui04)
                    st.dataframe(df_Rnge)
                else:
                    msg_gui04 = ''
                    msg = f'No Range Dataframe for :{value.ticker}'
                    msg_gui04 = msg_gui04 + msg + '<br/>'
                    guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = msg_gui04)
                
                
                
            else:
                msg_gui04 = ''
                msg = f'No Data Analytic Dataframe for :{value.ticker}'
                msg_gui04 = msg_gui04 + msg + '<br/>'
                guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = msg_gui04)
            st.markdown('---')
            cnt += 1

                
            
            
            
            
            
            

