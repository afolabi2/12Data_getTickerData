import streamlit as st
import pandas as pd
import datetime
import get12Data as g12d
from io import StringIO 


# to run streamlit app
# streamlit run ./files.py/streamlit-app.py

# ====================
# SETTINGS FUNCTIONS
# ====================
# set page config options
# webpage for page_icons: https://emojipedia.org/search/?q=chart
st.set_page_config(page_title="Ticker Stream", 
                    page_icon="📈",
                    layout="wide", 
                    initial_sidebar_state="expanded" 
                    #,menu_items={
                    #'Get Help': 'https://www.extremelycoolapp.com/help',
                    #'Report a bug': "https://www.extremelycoolapp.com/bug",
                    #'About': "# This is a header. This is an *extremely* cool app!"}
                    ) #auto None

# settings to remove top right hamburger menu
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# settings to remove padding between components
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

# ====================
# HELPER FUNCTIONS
# ====================
#<font color=‘red’>THIS TEXT WILL BE RED</font>, unsafe_allow_html=True)

def colorMarkDown(fontcolor = '#33ff33', fontsze = 24, msg="Enter some Text"):
    # will need color to color coding map. default color '#33ff33' is green
    st.markdown(f'<h1 style="color:{fontcolor};font-size:{fontsze}px;">{msg}</h1>', unsafe_allow_html=True)

def sideBarcolorMarkDown(fontcolor = '#33ff33', fontsze = 24, msg="Enter some Text"):
    # will need color to color coding map. default color '#33ff33' is green
    st.sidebar.markdown(f'<h1 style="color:{fontcolor};font-size:{fontsze}px;">{msg}</h1>', unsafe_allow_html=True)

def colorHeader(fontcolor = '#33ff33', fontsze = 30, msg="Enter some Text"):
    # will need color to color coding map. default color '#33ff33' is green
    st.markdown(f'<h1 style="color:{fontcolor};font-size:{fontsze}px;">{msg}</h1>', unsafe_allow_html=True)

def sideBarcolorHeader(fontcolor = '#33ff33', fontsze = 30, msg="Enter some Text"):
    # will need color to color coding map. default color '#33ff33' is green
    st.sidebar.markdown(f'<h1 style="color:{fontcolor};font-size:{fontsze}px;">{msg}</h1>', unsafe_allow_html=True)

# ====================
# PRINT OUT FUNCTIONS
# ====================
def filterPrint(symbol_select, type_select, country_select, exchange_select ):
    #need to add hard limits to qty of tickers and date ranges here
    df_filter, symb_error_out_shre_lst, symb_error_flt_shre_lst = g12d.filter_tcker(apikey_12Data, stocks_df, symbol_select, 
                                        type_select, country_select, exchange_select)  
    st.session_state.messages = []    
    st.session_state.dataframe = [] 
    mess = f'Nos. of Tickers Processed with filter criteria: **{len(df_filter.index)}**'
    st.session_state.messages.append(mess)
    
    mess = f'Ticker Symbol(s) Selected: **{symbol_select}**'
    st.session_state.messages.append(mess)
    mess = f'     Ticker Type Selected: **{type_select}**'
    st.session_state.messages.append(mess)
    mess = f'         Country Selected: **{country_select}**'
    st.session_state.messages.append(mess)
    mess = f'          Exchange Select: **{exchange_select}**'
    st.session_state.messages.append(mess)            
    
    if len(symb_error_out_shre_lst) > 0:
        mess = f'data unavailable for {len(symb_error_out_shre_lst)} Nos. of Tickers'
        st.session_state.messages.append(mess)
        mess = symb_error_out_shre_lst
        st.session_state.messages.append(mess)
    if len(symb_error_flt_shre_lst) > 0:
        mess = f'data unavailable for {len(symb_error_flt_shre_lst)} Nos. of Tickers'
        st.session_state.messages.append(mess)
        mess = symb_error_flt_shre_lst
        st.session_state.messages.append(mess)
    st.session_state.dataframe.append(df_filter)

    with get12Data_expander:
        for msg in st.session_state.messages:
            st.markdown(msg)
        if "dataframe" in st.session_state: 
            msg = 'DataFrame for Filtered Ticker List'
            colorHeader(fontcolor = '#800080', fontsze = 18, msg = msg)
        for dataframe in st.session_state.dataframe:
            st.dataframe(dataframe)
    
    return df_filter, symb_error_out_shre_lst, symb_error_flt_shre_lst




# ====================
# DATAFRAME FORMATTING 
# ====================
pd.options.display.float_format = '{:,}'.format


# ====================
# API CALLS 
# ====================
@st.cache
def initialiseTickerLst(apikey_12Data):
    stocks_df = g12d.get_tck_stocks_df(apikey_12Data)
    return stocks_df

apikey_12Data = "7940a5c7698545e98f6617f235dd1d5d"
stocks_df = initialiseTickerLst(apikey_12Data)
total_rows_unfiltered_tickername_12Data = len(stocks_df)
get12Data_expander = st.expander(f"12Data OutPut")
with get12Data_expander:
    msg = 'Tickers Available from 12Data'
    colorHeader(fontcolor = '#800080', fontsze = 18, msg = msg)
    st.markdown(f'total nos of tickers available: **{total_rows_unfiltered_tickername_12Data:,}**')
if "messages" not in st.session_state:      
    st.session_state.messages = []    
if "dataframe" not in st.session_state: 
    st.session_state.dataframe = []   
if "toProcessInput" not in st.session_state: 
    st.session_state.toProcessInput = []   
# ====================
# SIDE BAR AREA 
# ====================
msg = 'VARIABLES'
sideBarcolorHeader(fontcolor = '#0000FF', fontsze = 20, msg = msg)
st.sidebar.markdown("---")
#DataSource Radio Buttons
# inst_type will be stored
msg = 'INSTRUMENT SELECTION'
sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
inst_lst   = ["Stock Ticker", "(Not Ready)Crypto Currency"]
inst_radio = st.sidebar.radio("Please select an Instrument Type", inst_lst)
st.sidebar.write(f"**{inst_radio} Data selected**")
st.sidebar.markdown("---")



if inst_radio == "Stock Ticker":
    #DataSource Radio Buttons
    #data_src will be stored
    msg = 'DATA SOURCE SELECTION'
    sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
    datasrc_lst = ["12 Data", "(Not Ready)Alpha-Vantage", "(Not Ready)Alpaca"]
    src_radio = st.sidebar.radio("Stock Data API", datasrc_lst) 
    st.sidebar.write(f"**{src_radio} API selected**")
    st.sidebar.markdown("---")

    if src_radio == "12 Data":
        msg = 'API KEY INPUT'
        sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
        ApiKey_lst = ["Default", "Enter API Key", "(Not Ready)Use Envir Stored Variable '12DataApiKey'", "(Not Ready)Get api from file"]
        ApiKey_radio = st.sidebar.radio("Please provide API Key", ApiKey_lst)
   
        if ApiKey_radio == "Default":
            st.sidebar.write(f'**{ApiKey_radio} 12Data API Key will be used**')
        elif ApiKey_radio == "Enter API Key":
            apikey_12Data = st.sidebar.text_input('Please Enter 12 Data API Key', 'Please Enter 12 Data API Key')
        st.sidebar.markdown("---")

        msg = 'TICKER SELECTION'
        sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)

        tcker_select_type_lst   = ["Single or Multiple Ticker(s) Symbols", "Load Ticker(s) Symbols from File"]
        tcker_select_type_radio = st.sidebar.radio("How do you want to select your Ticker", tcker_select_type_lst)
        
        if tcker_select_type_radio == "Load Ticker(s) Symbols from File":
            symbol_select = []
            st.sidebar.write(f"***Please Make sure file contents are comma delimited***") 
            uploaded_file = st.sidebar.file_uploader("Choose a file for Ticker Symbol(s)")
            if uploaded_file is not None:
                # To read file as string:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                string_data = stringio.read()
                tcker_lst = g12d.get_tcker_lst_fromStringIO(string_data)
                    
                illegal_tcker = list(set(tcker_lst) - set(stocks_df.symbol))
                legal_tcker   = list(set(tcker_lst) - set(illegal_tcker))

                if len(legal_tcker) > 0:
                    symbol_lst = legal_tcker
                    symbol_select = st.sidebar.multiselect('Symbol list from file will appear here', symbol_lst, symbol_lst )

                if len(illegal_tcker) > 0:
                    with get12Data_expander:
                        st.markdown(f"Nos. of Illegal tickers: **{len(illegal_tcker)}**")
                        st.markdown(f'Ticker List: **{illegal_tcker}**')
                        st.markdown("---")
                if len(legal_tcker) > 0:
                    with get12Data_expander:
                        st.markdown(f"Nos. of Legal tickers: **{len(legal_tcker)}**")
                        st.markdown(f'Ticker List: **{legal_tcker}**')
                        st.markdown("---") 

        elif (tcker_select_type_radio == "Single or Multiple Ticker(s) Symbols"):
            symbol_lst = g12d.get_tcker_symbol_lst(stocks_df)
            symbol_select = st.sidebar.multiselect('Type in the ticker symbol here', options = symbol_lst)

            with get12Data_expander:
                st.markdown(f"Nos. of Legal tickers: **{len(symbol_select)}**")
                st.markdown(f'Ticker List: **{symbol_select}**')
                st.markdown("---")
        
        st.sidebar.markdown("---")
        msg = 'FILTER SELECTION'
        sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)

        type_lst = g12d.get_tcker_type_lst(stocks_df)
        type_select = st.sidebar.multiselect('Type in the ticker type here', 
                                            options = type_lst,
                                            default = ["Common", "Common Stock", "EQUITY"])    

        country_lst = g12d.get_tcker_country_lst(stocks_df)
        country_select = st.sidebar.multiselect('Type in the ticker country here', 
                                                options = country_lst,
                                                default = ["United States"])
        exchange_lst = g12d.get_tcker_exchange_lst(stocks_df)
        exchange_select = st.sidebar.multiselect('Type in the ticker exchange here',
                                                options = exchange_lst,
                                                default = ["NASDAQ"])
        
        
        
        filter_submit = st.sidebar.button('Submit Filter Selection')
        if filter_submit:
            df_filter, symb_error_out_shre_lst, symb_error_flt_shre_lst = filterPrint(symbol_select, type_select, country_select, exchange_select )
            st.sidebar.markdown("---")

        msg = 'STOCK INTERVAL SELECTION'
        sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
        interval = st.sidebar.select_slider('Select Stock Data Interval',
                                options=['1min', '5min', '15min', '30min', '45min', '1h', '2h', '4h', '1day', '1week', '1month'])
        st.sidebar.write(f'**Selected Stock Data Interval is {interval}**')
        st.sidebar.markdown("---")        

        #st.markdown("""### TIME RANGE SELECTION\START DATE""")
        #timeRangeOption = st.selectbox('Please select type of Time Range Selection',
        #                                ('earliestTimeStamp_todaysDate',
        #                                'earliestTimeStamp_userEndDate',
        #                                'earliestTimeStamp_timeRange',
        #                                'userStartDate_todaysDate',
        #                                'userStartDate_timeRange',
        #                                'userEndDate_timeRange',
        #                                'userStartDate_userEndDate'))
        #st.write('You selected:', timeRangeOption)
        #st.markdown("---")

        msg = 'TIME RANGE SELECTION: START DATE'
        sideBarcolorMarkDown(fontcolor = '#800080', fontsze = 14, msg = msg)
        approvedDateInputType = ('user provided StartDate', 'user provided EndDate')
        AllTimeRngeTuple = ('earliestTimeStamp','user provided StartDate', 'user provided EndDate', 'Time Interval', "Today's Date")

        
        startTimeRngeTuple = ('earliestTimeStamp','user provided StartDate', "Today's Date")
        startTimeRangeOption = st.sidebar.selectbox('Please select type of Start Date', startTimeRngeTuple )

        if startTimeRangeOption in approvedDateInputType:
            start_date_input = st.sidebar.date_input("Select Start Date", datetime.date.today())
            st.sidebar.write('Start Date is:', start_date_input)
        elif startTimeRangeOption ==  "Today's Date":
            today_date_input = datetime.date.today()
            st.sidebar.write('Start Date is:', today_date_input)
        elif startTimeRangeOption ==  "earliestTimeStamp":
            st.sidebar.write(f'We will Calculate Start Date from {startTimeRangeOption}')
        st.sidebar.markdown("---")

        msg = 'TIME RANGE SELECTION: END DATE'
        sideBarcolorMarkDown(fontcolor = '#800080', fontsze = 14, msg = msg)
        EndTimeRngeTuple = ('earliestTimeStamp','user provided StartDate', 'user provided EndDate', 'Time Interval', "Today's Date" )
        if startTimeRangeOption == 'earliestTimeStamp':
            EndTimeRngeTuple = ('user provided EndDate', 'Time Interval', "Today's Date")
        elif startTimeRangeOption == 'user provided StartDate':
            EndTimeRngeTuple = ('user provided EndDate', 'Time Interval', "Today's Date")
        #elif startTimeRangeOption == 'user provided EndDate':
        #    EndTimeRngeTuple = ('earliestTimeStamp', 'user provided StartDate', 'Time Interval', "Today's Date")
        #elif startTimeRangeOption == 'Time Interval':
        #    EndTimeRngeTuple = ('earliestTimeStamp', 'user provided StartDate', 'user provided EndDate', "Today's Date")
        elif startTimeRangeOption == "Today's Date":
            EndTimeRngeTuple = ("Time Interval",  "Today's Date")
            
        endTimeRangeOption = st.sidebar.selectbox('Please select type of End Date', EndTimeRngeTuple )

        if endTimeRangeOption in approvedDateInputType:
            end_date_input = st.sidebar.date_input("Select End Date", datetime.date.today())
            st.sidebar.write('End Date is:', end_date_input)

        elif endTimeRangeOption ==  "Today's Date":
            st.sidebar.write('End Date is:', datetime.date.today())
        elif endTimeRangeOption ==  "Time Interval":
            timeIntervalUnit = st.sidebar.selectbox('Please select Time Interval Unit?',('seconds', 'minutes', 'hours', 'days', 'weeks', 'months', 'years'))
            timeIntervalValue = st.sidebar.number_input('Insert a Time Interval Value', min_value = 1)
            st.sidebar.write(f'Selected Time Interval is {timeIntervalValue} {timeIntervalUnit}')
        else:
            st.sidebar.write(f'We will Calculate End Date from {endTimeRangeOption}')
        
        getTmeRnge = f'{startTimeRangeOption}-{endTimeRangeOption}'
    st.sidebar.markdown("---")

# ====================
# MAIN AREA 
# ====================
use12Data_expander = st.expander(f"12Data Input for Time Series Computations")

if st.sidebar.button('Submit'):
    #need to add hard limits to qty of tickers and date ranges here
    if not filter_submit:
        print("this is some bullshit")
        df_filter, symb_error_out_shre_lst, symb_error_flt_shre_lst = filterPrint(symbol_select, type_select, country_select, exchange_select )
    
    if len(symbol_select) == 0:
                st.warning('Please populate ticker symbol')
    else:
        st.session_state.toProcessInput = []  
        mess = f'Instrument Type selected: {inst_radio}'
        st.session_state.toProcessInput.append(mess) 
        mess = f'Data Source selected: {src_radio}'
        st.session_state.toProcessInput.append(mess) 
        mess = f'API Key to use: {ApiKey_radio}'
        st.session_state.toProcessInput.append(mess) 
        mess = f'Ticker Symbol(s) Selected: {symbol_select}'
        st.session_state.toProcessInput.append(mess) 
        mess = f'Time Interval to use: {interval}'
        st.session_state.toProcessInput.append(mess) 
        mess = f'Time Range to procure Data: {getTmeRnge}'
        st.session_state.toProcessInput.append(mess)

        mess = f'Time Range Start type is: {startTimeRangeOption}'
        st.session_state.toProcessInput.append(mess)
        mess = f'Time Range End Type is: {endTimeRangeOption}'
        st.session_state.toProcessInput.append(mess)
        mess = f'---'
        st.session_state.toProcessInput.append(mess)

        for symbol in symbol_select:
            if startTimeRangeOption == 'earliestTimeStamp':
                date = g12d.getTickerEarliesrTimeStamp(apikey_12Data, symbol, interval)
                mess = f'earliestTimeStamp for {symbol}: {date}'
                st.session_state.toProcessInput.append(mess)
                final_start_date = date['datetime_data']
            if startTimeRangeOption == 'user provided StartDate':
                mess = f'user provided StartDate input: {start_date_input}'
                st.session_state.toProcessInput.append(mess) 
                final_start_date = start_date_input
            if startTimeRangeOption == "Today's Date":
                mess = f'Todays Date input: {today_date_input}'
                st.session_state.toProcessInput.append(mess) 
                final_start_date = today_date_input


            if endTimeRangeOption == 'user provided EndDate':
                mess = f'user provided EndDate input: {end_date_input}'
                st.session_state.toProcessInput.append(mess)
                final_end_date = end_date_input    
            if endTimeRangeOption == "Time Interval":
                mess = f'Time Interval Value is: {timeIntervalValue} {timeIntervalUnit}'
                st.session_state.toProcessInput.append(mess) 
                final_end_date = g12d.addRelTimeDelta(final_start_date, timeIntervalValue, timeIntervalUnit)
            if endTimeRangeOption == "Today's Date":
                mess = f'Todays Date input: {today_date_input}'
                st.session_state.toProcessInput.append(mess) 
                final_end_date = today_date_input
            mess = f'Time Series Computations Date Range| Start Date: {final_start_date} | End Date: {final_end_date}  '
            st.session_state.toProcessInput.append(mess) 
            mess = f'---'
            st.session_state.toProcessInput.append(mess)

        with use12Data_expander:
            if len(st.session_state.toProcessInput) != 0:
                mess = f'Data to be passed on for Time Series Computations'
                colorHeader(fontcolor = '#800080', fontsze = 20, msg = mess)
            for msg in st.session_state.toProcessInput:
                colorHeader(fontcolor = '#00008B', fontsze = 12, msg = msg)
            
else:
    pass
     #st.write('Goodbye')






            



        
    

    
