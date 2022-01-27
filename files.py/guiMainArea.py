import streamlit as st
import pandas as pd

# programmatic calculations
import get12Data as g12d
import getAnalytics as gAna




# gui helper functions
import guiMarkDown as guiMrk #used for markdown and write functions
import guiLogic as guiLgc #used for function calls outside of

def initSessionStates():
    if "trans_df" not in st.session_state: 
        st.session_state.trans_df = pd.DataFrame() 
    if "Rnge_df" not in st.session_state: 
        st.session_state.Rnge_df = pd.DataFrame() 
    if "Voltle_df" not in st.session_state: 
        st.session_state.Voltle_df = pd.DataFrame() 



    if "df_filter" not in st.session_state: 
        st.session_state.df_filter = [] 
    if "df_use12Data" not in st.session_state: 
        st.session_state.df_use12Data = [] 
    if "df_12TSD" not in st.session_state: 
        st.session_state.df_12TSD = [] 
    if "res_dct" not in st.session_state: 
        st.session_state.res_dct = [] 
    


    if "msg_get12Data" not in st.session_state: 
        st.session_state.msg_get12Data = ''  
    if "msg_use12Data" not in st.session_state: 
        st.session_state.msg_use12Data = '' 
    if "msg_get12TSD" not in st.session_state: 
        st.session_state.msg_get12TSD = '' 
    if "msg_getANN" not in st.session_state: 
        st.session_state.msg_getANN = ''





    if "get12Data_expander" not in st.session_state: 
        st.session_state.get12Data_expander = st.delta_generator.DeltaGenerator  
    if "use12Data_expander" not in st.session_state: 
        st.session_state.use12Data_expander = st.delta_generator.DeltaGenerator  
    if "get12TSD_expander" not in st.session_state: 
        st.session_state.get12TSD_expander = st.delta_generator.DeltaGenerator  
    if "getAnalytics_expander" not in st.session_state: 
        st.session_state.getAnalytics_expander = st.delta_generator.DeltaGenerator  

def filterPrint():
    df_filter, symb_error_out_shre_lst, symb_error_flt_shre_lst = g12d.filter_tcker(st.session_state.Data12_PaidKey, 
                                                            st.session_state.df_stock, st.session_state.symbol_select, 
                                                            st.session_state.type_select, st.session_state.country_select, 
                                                            st.session_state.exchange_select)  
    st.session_state.df_filter = [] 
    st.session_state.df_filter.append(df_filter)
    return df_filter, symb_error_out_shre_lst, symb_error_flt_shre_lst

def writeGet12(symb_error_out_shre_lst, symb_error_flt_shre_lst ):
    msg_get12Data = ''
    if len(symb_error_out_shre_lst) > 0:
        msg = f'outstanding shares data unavailable for {len(symb_error_out_shre_lst)} Nos. of Tickers'
        msg_get12Data = msg_get12Data + msg + '<br/>'
        msg = symb_error_out_shre_lst
        msg_get12Data = msg_get12Data + msg + '<br/>'
    if len(symb_error_flt_shre_lst) > 0:
        msg = f'floating shares data unavailable for {len(symb_error_flt_shre_lst)} Nos. of Tickers'
        msg_get12Data = msg_get12Data + msg + '<br/>'
        msg = symb_error_flt_shre_lst
        msg_get12Data = msg_get12Data + msg + '<br/>'
    msg = f"Nos. of Legal tickers: {len(st.session_state.symbol_select)}"
    msg_get12Data = msg_get12Data + msg + '<br/>'
    msg = f'Ticker List: **{st.session_state.symbol_select}'
    msg_get12Data = msg_get12Data + msg + '<br/>'

    st.session_state.msg_get12Data = msg_get12Data

    with st.session_state.get12Data_expander:
        msg = 'Tickers Available from 12Data'
        guiMrk.colorHeader(fontcolor = '#800080', fontsze = 18, msg = msg)
        guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = st.session_state.msg_get12Data)

        if "dataframe" in st.session_state: 
            msg = 'DataFrame for Filtered Ticker List'
            guiMrk.colorHeader(fontcolor = '#800080', fontsze = 18, msg = msg)
        for dataframe in st.session_state.df_filter:
            st.dataframe(dataframe)

def writeUse12():
    if len(st.session_state.symbol_select) == 0:
                st.warning('Please populate ticker symbol')
    else:
        st.session_state.df_use12Data = []
        msg_use12Data = ''
        for symbol in st.session_state.symbol_select:
            if st.session_state.startTimeRangeOption == 'earliestTimeStamp':
                date_info = g12d.getTickerEarliesrTimeStamp(apikey_12Data, symbol)
                final_start_date_str = date_info['datetime_data']
                final_start_date = g12d.convertDateStrLen10toDateTime(final_start_date_str)

            if st.session_state.startTimeRangeOption == 'user provided StartDate':
                final_start_date_str = g12d.convertDateTimeToDateStrLen10(st.session_state.start_date_input)
                final_start_date =  g12d.convertDateStrLen10toDateTime(final_start_date_str)
            if st.session_state.startTimeRangeOption == "Today's Date":
                final_start_date_str = g12d.convertDateTimeToDateStrLen10(today_date_input)
                final_start_date = g12d.convertDateStrLen10toDateTime(final_start_date_str)

            if st.session_state.endTimeRangeOption == 'user provided EndDate':
                final_end_date_str = g12d.convertDateTimeToDateStrLen10(st.session_state.end_date_input)
                final_end_date = g12d.convertDateStrLen10toDateTime(final_end_date_str)

            if st.session_state.endTimeRangeOption == "Time Interval":
                final_end_date = g12d.addRelTimeDelta(final_start_date, timeIntervalValue, timeIntervalUnit)
                final_end_date_str = g12d.convertDateTimeToDateStrLen10(final_end_date)
            if st.session_state.endTimeRangeOption == "Today's Date":
                final_end_date_str = g12d.convertDateTimeToDateStrLen10(today_date_input)
                final_end_date = g12d.convertDateStrLen10toDateTime(final_end_date_str)
            
            symb_startEnd_df,maxRequestPerDay_freekey = g12d.getStartStopRngeLst(symbol, st.session_state.interval, final_start_date, final_end_date) 
            nosOfLoopsPerSymb = len(symb_startEnd_df.index)
            st.session_state.df_use12Data.append(symb_startEnd_df)
 
            if nosOfLoopsPerSymb > maxRequestPerDay_freekey:
                msg = f'{nosOfLoopsPerSymb} Required Time Series Requests exceeds Daily Free API Limit of {maxRequestPerDay_freekey} Requests for {symbol}'
                msg_use12Data = msg_use12Data + msg + '<br/>'
            else:
                msg = f'{nosOfLoopsPerSymb} Required Time Series Requests wont exceed Daily Free API Limit of {maxRequestPerDay_freekey} Requests for {symbol}'
                msg_use12Data = msg_use12Data + msg + '<br/>'
            
        return msg_use12Data




# ====================
# MAIN AREA 
# ====================
def get12main():
    #initialize session states to be used
    initSessionStates()
    
    st.session_state.get12Data_expander = st.expander(f"12Data Tickerlist Dataframe containing Outstanding & Float Shares")
    if st.session_state.filter_submit:
        df_filter, symb_error_out_shre_lst, symb_error_flt_shre_lst = filterPrint()
        st.sidebar.markdown("---")
        writeGet12(symb_error_out_shre_lst, symb_error_flt_shre_lst )
    elif st.session_state.button_submit:
        if not st.session_state.filter_submit:
            df_filter, symb_error_out_shre_lst, symb_error_flt_shre_lst = filterPrint()
            st.sidebar.markdown("---")
            writeGet12(symb_error_out_shre_lst, symb_error_flt_shre_lst )
            
def use12main():
    if st.session_state.button_submit:
        initSessionStates()

        st.session_state.use12Data_expander = st.expander(f"12Data Input for Time Series Computations")            

        msg_use12Data = writeUse12()

        allSymb_startEnd_lst = st.session_state.df_use12Data
        #get number of tickers to be used
        nosOfTickers = len(allSymb_startEnd_lst)
        msg = f'Nos of Ticker Symbol(s) to process: {nosOfTickers}' + '<br/>'
        msg_use12Data = msg + msg_use12Data
        # writing of data
        st.session_state.msg_use12Data = msg_use12Data
        with st.session_state.use12Data_expander:
            mess = f'Ticker Dataframes for Start Stop Date Ranges'
            guiMrk.colorHeader(fontcolor = '#800080', fontsze = 20, msg = mess)
            guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = st.session_state.msg_use12Data)

            cnt = 0
            len1 = len(st.session_state.df_use12Data)
            len2 = len(st.session_state.symbol_select)
            for dataframe in st.session_state.df_use12Data:
                symbol_select = st.session_state.symbol_select
                symbol = symbol_select[cnt]
                st.write('*' * 60)
                mess = f'{symbol} Requests Start Stop Date Range DataFrame'
                guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = mess)
                st.dataframe(dataframe)
                cnt+=1
            st.write('*' * 60)
            
def get12TSDmain():
    if st.session_state.button_submit:
        st.session_state.get12TSD_expander = st.expander(f"12Data Output for Time Series Computations")        
        msg_get12TSD = ''
        cnt = 0
        allSymb_startEnd_lst = st.session_state.df_use12Data
        symbol_select = st.session_state.symbol_select
        for symbStartEnd in allSymb_startEnd_lst:
            curr_symb   = symbol_select[cnt]
            lenOfDf = len(symbStartEnd.index)
            first_start = symbStartEnd.start_time[0]
            last_end    = symbStartEnd.end_time[lenOfDf - 1]
            msg = f'Time Series Data for {curr_symb} Will run {lenOfDf} Times from {first_start} to {last_end}'
            msg_get12TSD = msg_get12TSD + msg + '<br/>'
            cnt += 1
        msg_get12TSD = msg_get12TSD +'<br/>'
        
        symbol_startend_dict = {
        "symbol":symbol_select, "start_stop_data": allSymb_startEnd_lst}

        res_dct = g12d.getAllSymbolTimeSeries_dfs(st.session_state.Data12_PaidKey, symbol_startend_dict)
        st.session_state.res_dct = res_dct
        #st.write(f'fire on the mountain')
        #st.write(res_dct)
        
        # add value df to session state
        st.session_state.df_12TSD = []
        for key, value in st.session_state.res_dct.items():
            st.session_state.df_12TSD.append(value.df_tsData)
     
        #msg_get12TSD = ''
        for key, value in st.session_state.res_dct.items():
            total_data_pts = len(value.df_tsData.index)
            msg = f'{value.ticker} Available Time Series Dataframe between {value.start_date} and {value.end_date}'
            msg_get12TSD = msg_get12TSD + msg + '<br/>'
        msg_get12TSD = msg_get12TSD +'<br/>'    

        for key, value in st.session_state.res_dct.items():    
            msg = f'{value.ticker} has Max Nos of DataPoints:{value.outputsize}'
            msg_get12TSD = msg_get12TSD + msg + '<br/>'
            msg = f'{value.ticker} has Total DataPoints:{total_data_pts}'
            msg_get12TSD = msg_get12TSD + msg + '<br/>'

        # writing of data
        cnt = 0
        st.session_state.msg_get12TSD = msg_get12TSD
        with st.session_state.get12TSD_expander:
            mess = f'Ticker Dataframes for Time Series Data'
            guiMrk.colorHeader(fontcolor = '#800080', fontsze = 20, msg = mess)            
            guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = st.session_state.msg_get12TSD)

            st.dataframe(st.session_state.df_12TSD[cnt])
            cnt += 1

def get12Analytics():   
    if st.session_state.button_submit:
        st.session_state.getAnalytics_expander = st.expander(f"Analytics for Time Series Computations")
        
        with st.session_state.getAnalytics_expander:
            mess = f'Ticker Dataframes for Analytics'
            guiMrk.colorHeader(fontcolor = '#800080', fontsze = 20, msg = mess)
            cnt1 = 0
            for key, value in st.session_state.res_dct.items():
                st.session_state.trans_df = gAna.analytics(value.df_tsData)
                msg_getANN = ''
                msg = f'Data Analytic Dataframe for :{value.ticker}'
                msg_getANN = msg_getANN + msg + '<br/>'
                guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = msg_getANN)
                st.dataframe(st.session_state.trans_df)
                
                
                st.session_state.Rnge_df = gAna.df_filter_Range(st.session_state.trans_df)
                if len(st.session_state.Rnge_df.index) > 0:
                    msg_getANN = ''
                    msg = f'Range Dataframe for :{value.ticker}'
                    msg_getANN = msg_getANN + msg + '<br/>'
                    guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = msg_getANN)
                    st.dataframe(st.session_state.Rnge_df)
                else:
                    msg_getANN = ''
                    msg = f'No Range Dataframe for :{value.ticker}'
                    msg_getANN = msg_getANN + msg + '<br/>'
                    guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = msg_getANN)
                
                
                # get min and max value range to use as range filters for dataframe volatile column data
                st.markdown('---')
                minVal, maxVal = gAna.df_getMinMaxVal_Volatile(st.session_state.trans_df)
                st.write(f'min value: {minVal} <br/> max value {maxVal}')
                volatile_slide = st.slider('Min and Max Volatile Column Range?', value = [minVal, maxVal])
                cnt1 += 1


                #st.session_state.Voltle_df = gAna.df_filter_Volatile(st.session_state.trans_df, minVal, maxVal)
                #if len(st.session_state.Voltle_df.index) > 0:
                #    msg_getANN = ''
                #    msg = "*" * 60
                #    msg_getANN = msg_getANN + msg + '<br/>'
                #    msg = f'Volatile Dataframe for :{value.ticker}'
                #    msg_getANN = msg_getANN + msg + '<br/>'
                #    msg = f'Volatile column values range between {minVal} - {maxVal}'
                #    msg_getANN = msg_getANN + msg + '<br/>'
                #    guiMrk.colorHeader(fontcolor = '#00008B', fontsze = 12, msg = msg_getANN)
                #    st.dataframe(st.session_state.Voltle_df)
