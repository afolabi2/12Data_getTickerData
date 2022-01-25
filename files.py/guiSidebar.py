import streamlit as st
import datetime

# gui helper functions
import guiMarkDown as guiMrk #used for markdown and write functions
import guiLogic as guiLgc #used for function calls outside of

# programmatic calculations
import get12Data as g12d


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
    if "filter_submit" not in st.session_state: 
        st.session_state.filter_submit = False
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

    if "dataframe" not in st.session_state: 
        st.session_state.df_filter = []   


    



    #if "df_use12Data" not in st.session_state: 
    #    st.session_state.df_use12Data = []  
    #if "symb_lst" not in st.session_state: 
    #    st.session_state.symb_lst = []  
    #if "df_12TSD" not in st.session_state: 
    #    st.session_state.df_12TSD = []

def sideGui():
    # ====================
    # SIDE BAR AREA 
    # ====================
    #initialize session states to be used
    initSessionStates()
    
    #DataSource Radio Buttons
    # inst_type will be stored
    msg = 'INSTRUMENT SELECTION'
    guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
    inst_lst   = ["Stock Ticker", "(Not Ready)Crypto Currency"]
    st.session_state.inst_radio = st.sidebar.radio("Please select an Instrument Type", inst_lst)
    st.sidebar.write(f"**{st.session_state.inst_radio} Data selected**")
    st.sidebar.markdown("---")

    if st.session_state.inst_radio == "Stock Ticker":
        #DataSource Radio Buttons
        #data_src will be stored
        msg = 'DATA SOURCE SELECTION'
        guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
        datasrc_lst = ["12 Data", "(Not Ready)Alpha-Vantage", "(Not Ready)Alpaca"]
        st.session_state.src_radio = st.sidebar.radio("Stock Data API", datasrc_lst) 
        st.sidebar.write(f"**{st.session_state.src_radio} API selected**")
        st.sidebar.markdown("---")  

        if st.session_state.src_radio == "12 Data":
            msg = 'API KEY INPUT'
            guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
            ApiKey_lst = ["Default", "Enter API Key", "(Not Ready)Use Envir Stored Variable '12DataApiKey'", "(Not Ready)Get api from file"]
            st.session_state.apikey_radio = st.sidebar.radio("Please provide API Key", ApiKey_lst)
   
            if st.session_state.apikey_radio == "Default":
                st.sidebar.write(f'**{st.session_state.apikey_radio} 12Data API Key will be used**')
            elif st.session_state.apikey_radio == "Enter API Key":
                apikey_12Data = st.sidebar.text_input('Please Enter 12 Data API Key', 'Please Enter 12 Data API Key')
            st.sidebar.markdown("---")

            msg = 'TICKER SELECTION'
            guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)

            tcker_select_type_lst   = ["Single or Multiple Ticker(s) Symbols", "Load Ticker(s) Symbols from File"]
            st.session_state.tckseltyp_radio = st.sidebar.radio("How do you want to select your Ticker", tcker_select_type_lst)

            if st.session_state.tckseltyp_radio == "Load Ticker(s) Symbols from File":
                st.session_state.symbol_select = []
                st.sidebar.write(f"***Please Make sure file contents are comma delimited***") 
                uploaded_file = st.sidebar.file_uploader("Choose a file for Ticker Symbol(s)")

                if uploaded_file is not None:
                    illegal_tcker, legal_tcker = readFileasStr(uploaded_file)
                    if len(legal_tcker) > 0:
                        symbol_lst = legal_tcker
                        st.session_state.symbol_select = st.sidebar.multiselect('Symbol list from file will appear here', symbol_lst, symbol_lst )
                      

            elif (st.session_state.tckseltyp_radio == "Single or Multiple Ticker(s) Symbols"):
                stocks_df = st.session_state.df_stock
                symbol_lst = g12d.get_tcker_symbol_lst(stocks_df)
                st.session_state.symbol_select = st.sidebar.multiselect('Type in the ticker symbol here', options = symbol_lst, default = ["MITQ"])  # DEFAULT FOR TESTING

            st.sidebar.markdown("---")
            msg = 'FILTER SELECTION'
            guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)

            type_lst = g12d.get_tcker_type_lst(stocks_df)
            st.session_state.type_select = st.sidebar.multiselect('Type in the ticker type here', 
                                                options = type_lst,
                                                default = ["Common Stock"])   
                                                #default = ["Common", "Common Stock", "EQUITY"]) seems 12data removed the common and equity options

            country_lst = g12d.get_tcker_country_lst(stocks_df)
            st.session_state.country_select = st.sidebar.multiselect('Type in the ticker country here', 
                                                    options = country_lst,
                                                    default = ["United States"])

            exchange_lst = g12d.get_tcker_exchange_lst(stocks_df)
            st.session_state.exchange_select = st.sidebar.multiselect('Type in the ticker exchange here',
                                                    options = exchange_lst,
                                                    default = ["NASDAQ", "CBOE", "NYSE", "OTC"])

            st.session_state.filter_submit = st.sidebar.button('Submit Filter Selection')
            
            msg = 'STOCK INTERVAL SELECTION'
            guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
            st.session_state.interval = st.sidebar.select_slider('Select Stock Data Interval',
                                    options=['1min', '5min', '15min', '30min', '45min', '1h', '2h', '4h', '1day', '1week', '1month'])
            st.sidebar.write(f'**Selected Stock Data Interval is {st.session_state.interval}**')
            st.sidebar.markdown("---")    

            msg = 'TIME RANGE SELECTION: START DATE'
            guiMrk.sideBarcolorMarkDown(fontcolor = '#800080', fontsze = 14, msg = msg)
            
            # assigning tuples to use
            approvedDateInputType = ('user provided StartDate', 'user provided EndDate')
            AllTimeRngeTuple = ('user provided StartDate', 'earliestTimeStamp','user provided EndDate', 'Time Interval', "Today's Date")

            startTimeRngeTuple = ('user provided StartDate', 'earliestTimeStamp', "Today's Date")
            st.session_state.startTimeRangeOption = st.sidebar.selectbox('Please select type of Start Date', startTimeRngeTuple )

            if st.session_state.startTimeRangeOption in approvedDateInputType:
                st.session_state.start_date_input = st.sidebar.date_input("Select Start Date", datetime.date(2022, 1, 1)) # FOR TESTING
                #start_date_input = st.sidebar.date_input("Select Start Date", datetime.date.today())
                st.sidebar.write('Start Date is:', st.session_state.start_date_input)

            elif st.session_state.startTimeRangeOption ==  "Today's Date":
                today_date_input = datetime.date.today()
                st.sidebar.write('Start Date is:', today_date_input)

            elif st.session_state.startTimeRangeOption ==  "earliestTimeStamp":
                st.sidebar.write(f'We will Calculate Start Date from {st.session_state.startTimeRangeOption}')
            st.sidebar.markdown("---")

            msg = 'TIME RANGE SELECTION: END DATE'
            guiMrk.sideBarcolorMarkDown(fontcolor = '#800080', fontsze = 14, msg = msg)
            EndTimeRngeTuple = guiLgc.getEndTimeRngeTuple(st.session_state.startTimeRangeOption)
            st.session_state.endTimeRangeOption = st.sidebar.selectbox('Please select type of End Date', EndTimeRngeTuple )

            if st.session_state.endTimeRangeOption in approvedDateInputType:
                st.session_state.end_date_input = st.sidebar.date_input("Select End Date", datetime.date.today())
                st.sidebar.write('End Date is:', st.session_state.end_date_input)

            elif st.session_state.endTimeRangeOption ==  "Today's Date":
                today_date_input = datetime.date.today()
                st.sidebar.write('End Date is:', datetime.date.today())

            elif st.session_state.endTimeRangeOption ==  "Time Interval":
                timeIntervalUnit = st.sidebar.selectbox('Please select Time Interval Unit?',('seconds', 'minutes', 'hours', 'days', 'weeks', 'months', 'years'))
                timeIntervalValue = st.sidebar.number_input('Insert a Time Interval Value', min_value = 1)
                st.sidebar.write(f'Selected Time Interval is {timeIntervalValue} {timeIntervalUnit}')

            else:
                st.sidebar.write(f'We will Calculate End Date from {st.session_state.endTimeRangeOption}')

        st.sidebar.markdown("---")
    st.session_state.button_submit = st.sidebar.button('Submit')
    
    






                    # #get12Data_expander messages
                    # msg_get12Data = ''  
                    # total_rows_unfiltered_tickername_12Data = len(st.session_state.df_stock)
                    # msg = f'total nos of tickers available:{total_rows_unfiltered_tickername_12Data:,}'
                    # msg_get12Data = msg_get12Data + msg + '<br/>'
                    
                    ##get12Data_expander messages  
                    #if len(illegal_tcker) > 0:
                    #    msg = f'Nos. of Illegal tickers: {len(illegal_tcker)}'
                    #    msg_get12Data = msg_get12Data + msg + '<br/>'
                    #    msg = f'Ticker List: {illegal_tcker}'
                    #    msg_get12Data = msg_get12Data + msg + '<br/>'
                    #if len(legal_tcker) > 0:
                    #    msg = f'Nos. of legal tickers: {len(illegal_tcker)}'
                    #    msg_get12Data = msg_get12Data + msg + '<br/>'
                    #    msg = f'Ticker List: {legal_tcker}'
                    #    msg_get12Data = msg_get12Data + msg + '<br/>'









