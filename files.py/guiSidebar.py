import streamlit as st
import pandas as pd
import datetime
from io import StringIO 

# gui helper functions
import guiMarkDown as guiMrk #used for markdown and write functions

# programmatic calculations
import get12Data as g12d
import getAnalytics as gAna



def initSessionStates():
    #state session objects for widgets
    if "inst_radio" not in st.session_state:      
        st.session_state.inst_radio = '' 
    if "src_radio" not in st.session_state:      
        st.session_state.src_radio = ''   
    if "apikey_radio" not in st.session_state:      
        st.session_state.apikey_radio = ''   
    if "tckseltyp_radio" not in st.session_state:      
        st.session_state.tckseltyp_radio = ''
    if "symbol_select" not in st.session_state:      
        st.session_state.symbol_select = ''
    if "type_select" not in st.session_state:      
        st.session_state.type_select = ''
    if "country_select" not in st.session_state:      
        st.session_state.country_select = ''
    if "exchange_select" not in st.session_state:      
        st.session_state.exchange_select = ''
    if "startTimeRangeOption" not in st.session_state: 
        st.session_state.startTimeRangeOption = ''
    if "endTimeRangeOption" not in st.session_state: 
        st.session_state.endTimeRangeOption = ''
    if "start_date_input" not in st.session_state: 
        st.session_state.start_date_input = datetime.date
    if "end_date_input" not in st.session_state: 
        st.session_state.end_date_input = datetime.date


    if "button_submit" not in st.session_state: 
        st.session_state.button_submit = False

    if "interval" not in st.session_state: 
        st.session_state.interval = False

def readFileasStr(uploaded_file):
    # To read file as string:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    tcker_lst = g12d.get_tcker_lst_fromStringIO(string_data)

    illegal_tcker = list(set(tcker_lst) - set(stocks_df.symbol))
    legal_tcker   = list(set(tcker_lst) - set(illegal_tcker))

    return illegal_tcker, legal_tcker

def getEndTimeRngeTuple(startTimeRangeOption):
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
    return EndTimeRngeTuple




def sideGui():
    # ====================
    # SIDE BAR AREA 
    # ====================
    #initialize session states to be used
    initSessionStates()
    
    #DataSource Radio Buttons
    # inst_type will be stored
    sideBarform = st.sidebar.form("SideBar")
    msg = 'INSTRUMENT SELECTION'
    with sideBarform:
        guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
    
    inst_lst   = ["Stock Ticker", "(Not Ready)Crypto Currency"]
    st.session_state.inst_radio = sideBarform.radio("Please select an Instrument Type", inst_lst)
    with sideBarform:
        st.write(f"**{st.session_state.inst_radio} Data selected**")
    sideBarform.markdown("---")  
    if st.session_state.inst_radio == "Stock Ticker":
        #DataSource Radio Buttons
        #data_src will be stored
        msg = 'DATA SOURCE SELECTION'
        with sideBarform:
            guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
        datasrc_lst = ["12 Data", "(Not Ready)Alpha-Vantage", "(Not Ready)Alpaca"]
        st.session_state.src_radio = sideBarform.radio("Stock Data API", datasrc_lst) 
        with sideBarform:
            st.write(f"**{st.session_state.src_radio} API selected**")
        sideBarform.markdown("---")      
        if st.session_state.src_radio == "12 Data":
            msg = 'API KEY INPUT'
            with sideBarform:
                guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
            ApiKey_lst = ["Default", "Enter API Key", "(Not Ready)Use Envir Stored Variable '12DataApiKey'", "(Not Ready)Get api from file"]
            st.session_state.apikey_radio = sideBarform.radio("Please provide API Key", ApiKey_lst)

            if st.session_state.apikey_radio == "Default":
                with sideBarform:
                    st.write(f'**{st.session_state.apikey_radio} 12Data API Key will be used**')
            elif st.session_state.apikey_radio == "Enter API Key":
                apikey_12Data = sideBarform.text_input('Please Enter 12 Data API Key', 'Please Enter 12 Data API Key')
            sideBarform.markdown("---")  
            msg = 'TICKER SELECTION'
            with sideBarform:
                guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)   
            tcker_select_type_lst   = ["Single or Multiple Ticker(s) Symbols", "Load Ticker(s) Symbols from File"]
            st.session_state.tckseltyp_radio = sideBarform.radio("How do you want to select your Ticker", tcker_select_type_lst) 
            if st.session_state.tckseltyp_radio == "Load Ticker(s) Symbols from File":
                st.session_state.symbol_select = []
                with sideBarform:
                    st.write(f"***Please Make sure file contents are comma delimited***") 
                uploaded_file = sideBarform.file_uploader("Choose a file for Ticker Symbol(s)")  
                if uploaded_file is not None:
                    illegal_tcker, legal_tcker = readFileasStr(uploaded_file)
                    if len(legal_tcker) > 0:
                        symbol_lst = legal_tcker
                        st.session_state.symbol_select = sideBarform.multiselect('Symbol list from file will appear here', symbol_lst, symbol_lst )  
            elif (st.session_state.tckseltyp_radio == "Single or Multiple Ticker(s) Symbols"):
                stocks_df = st.session_state.df_stock
                symbol_lst = g12d.get_tcker_symbol_lst(stocks_df)
                st.session_state.symbol_select = sideBarform.multiselect('Type in the ticker symbol here', options = symbol_lst, default = ["MITQ"])  # DEFAULT FOR TESTING  
            sideBarform.markdown("---")
            msg = 'FILTER SELECTION'
            with sideBarform:
                guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)   
            type_lst = g12d.get_tcker_type_lst(stocks_df)
            st.session_state.type_select = sideBarform.multiselect('Type in the ticker type here', 
                                                options = type_lst,
                                                default = ["Common Stock"])   
                                                #default = ["Common", "Common Stock", "EQUITY"]) seems 12data removed the common and equity options 
            country_lst = g12d.get_tcker_country_lst(stocks_df)
            st.session_state.country_select = sideBarform.multiselect('Type in the ticker country here', 
                                                    options = country_lst,
                                                    default = ["United States"])    
            exchange_lst = g12d.get_tcker_exchange_lst(stocks_df)
            st.session_state.exchange_select = sideBarform.multiselect('Type in the ticker exchange here',
                                                    options = exchange_lst,
                                                    default = ["NASDAQ", "CBOE", "NYSE", "OTC"])    
            msg = 'STOCK INTERVAL SELECTION'
            with sideBarform:
                guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
            st.session_state.interval = sideBarform.select_slider('Select Stock Data Interval',
                                    options=['1min', '5min', '15min', '30min', '45min', '1h', '2h', '4h', '1day', '1week', '1month'])
            with sideBarform:
                st.write(f'**Selected Stock Data Interval is {st.session_state.interval}**')
            sideBarform.markdown("---")      
            msg = 'TIME RANGE SELECTION: START DATE'
            with sideBarform:
                guiMrk.sideBarcolorMarkDown(fontcolor = '#800080', fontsze = 14, msg = msg) 
            # assigning tuples to use
            approvedDateInputType = ('user provided StartDate', 'user provided EndDate')
            AllTimeRngeTuple = ('user provided StartDate', 'earliestTimeStamp','user provided EndDate', 'Time Interval', "Today's Date")    
            startTimeRngeTuple = ('user provided StartDate', 'earliestTimeStamp', "Today's Date")
            st.session_state.startTimeRangeOption = sideBarform.selectbox('Please select type of Start Date', startTimeRngeTuple )   
            if st.session_state.startTimeRangeOption in approvedDateInputType:
                st.session_state.start_date_input = sideBarform.date_input("Select Start Date", datetime.date(2022, 1, 1)) # FOR TESTING
                #start_date_input = sideBarform.date_input("Select Start Date", datetime.date.today())
                with sideBarform:
                    st.write('Start Date is:', st.session_state.start_date_input)   
            elif st.session_state.startTimeRangeOption ==  "Today's Date":
                today_date_input = datetime.date.today()
                with sideBarform:
                    st.write('Start Date is:', today_date_input)    
            elif st.session_state.startTimeRangeOption ==  "earliestTimeStamp":
                with sideBarform:
                    st.write(f'We will Calculate Start Date from {st.session_state.startTimeRangeOption}')
            sideBarform.markdown("---")  
            msg = 'TIME RANGE SELECTION: END DATE'
            with sideBarform:
                guiMrk.sideBarcolorMarkDown(fontcolor = '#800080', fontsze = 14, msg = msg)
            EndTimeRngeTuple = getEndTimeRngeTuple(st.session_state.startTimeRangeOption)
            st.session_state.endTimeRangeOption = sideBarform.selectbox('Please select type of End Date', EndTimeRngeTuple ) 
            if st.session_state.endTimeRangeOption in approvedDateInputType:
                st.session_state.end_date_input = sideBarform.date_input("Select End Date", datetime.date.today())
                with sideBarform:
                    st.write('End Date is:', st.session_state.end_date_input)   
            elif st.session_state.endTimeRangeOption ==  "Today's Date":
                today_date_input = datetime.date.today()
                with sideBarform:
                    st.write('End Date is:', datetime.date.today()) 
            elif st.session_state.endTimeRangeOption ==  "Time Interval":
                timeIntervalUnit = sideBarform.selectbox('Please select Time Interval Unit?',('seconds', 'minutes', 'hours', 'days', 'weeks', 'months', 'years'))
                timeIntervalValue = sideBarform.number_input('Insert a Time Interval Value', min_value = 1)
                with sideBarform:
                    st.write(f'Selected Time Interval is {timeIntervalValue} {timeIntervalUnit}')   
            else:
                with sideBarform:
                    st.write(f'We will Calculate End Date from {st.session_state.endTimeRangeOption}')  
        sideBarform.markdown("---")
    submit_butt = sideBarform.form_submit_button("Submit")
    st.session_state.button_submit = submit_butt
    
