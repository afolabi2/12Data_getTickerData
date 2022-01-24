import streamlit as st
import datetime

# gui helper functions
import guiMarkDown as guiMrk #used for markdown and write functions
import guiLogic as guiLgc #used for function calls outside of

# programmatic calculations
import get12Data as g12d
import getAnalytics as gAna

def sideGui():
    # ====================
    # SIDE BAR AREA 
    # ====================
    #DataSource Radio Buttons
    # inst_type will be stored
    msg = 'INSTRUMENT SELECTION'
    guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
    inst_lst   = ["Stock Ticker", "(Not Ready)Crypto Currency"]
    inst_radio = st.sidebar.radio("Please select an Instrument Type", inst_lst)
    st.sidebar.write(f"**{inst_radio} Data selected**")
    st.sidebar.markdown("---")
    # please add inst_radio value to a session state value

    if inst_radio == "Stock Ticker":
        #DataSource Radio Buttons
        #data_src will be stored
        msg = 'DATA SOURCE SELECTION'
        guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
        datasrc_lst = ["12 Data", "(Not Ready)Alpha-Vantage", "(Not Ready)Alpaca"]
        src_radio = st.sidebar.radio("Stock Data API", datasrc_lst) 
        st.sidebar.write(f"**{src_radio} API selected**")
        st.sidebar.markdown("---")  
        # please add src_radio value to a session state value 

        if src_radio == "12 Data":
            msg = 'API KEY INPUT'
            guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
            ApiKey_lst = ["Default", "Enter API Key", "(Not Ready)Use Envir Stored Variable '12DataApiKey'", "(Not Ready)Get api from file"]
            ApiKey_radio = st.sidebar.radio("Please provide API Key", ApiKey_lst)
    
            if ApiKey_radio == "Default":
                st.sidebar.write(f'**{ApiKey_radio} 12Data API Key will be used**')
            elif ApiKey_radio == "Enter API Key":
                apikey_12Data = st.sidebar.text_input('Please Enter 12 Data API Key', 'Please Enter 12 Data API Key')
            st.sidebar.markdown("---")
            # please add ApiKey_radio value to a session state value 

            msg = 'TICKER SELECTION'
            guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)

            tcker_select_type_lst   = ["Single or Multiple Ticker(s) Symbols", "Load Ticker(s) Symbols from File"]
            tcker_select_type_radio = st.sidebar.radio("How do you want to select your Ticker", tcker_select_type_lst)
            # please add tcker_select_type_radio value to a session state value

            if tcker_select_type_radio == "Load Ticker(s) Symbols from File":
                symbol_select = []
                st.sidebar.write(f"***Please Make sure file contents are comma delimited***") 
                uploaded_file = st.sidebar.file_uploader("Choose a file for Ticker Symbol(s)")

                if uploaded_file is not None:
                    illegal_tcker, legal_tcker = readFileasStr(uploaded_file)
                    if len(legal_tcker) > 0:
                        symbol_lst = legal_tcker
                        symbol_select = st.sidebar.multiselect('Symbol list from file will appear here', symbol_lst, symbol_lst )
                      

            elif (tcker_select_type_radio == "Single or Multiple Ticker(s) Symbols"):
                stocks_df = st.session_state.df_stock
                symbol_lst = g12d.get_tcker_symbol_lst(stocks_df)
                symbol_select = st.sidebar.multiselect('Type in the ticker symbol here', options = symbol_lst, default = ["MITQ"])  # DEFAULT FOR TESTING

                ##get12Data_expander messages  
                #msg = f"Nos. of Legal tickers: {len(symbol_select)}"
                #msg_get12Data = msg_get12Data + msg + '<br/>'
                #msg = f'Ticker List: **{symbol_select}'
                #msg_get12Data = msg_get12Data + msg + '<br/>'
            
            # please add symbol_select value to a session state value  

            st.sidebar.markdown("---")
            msg = 'FILTER SELECTION'
            guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)

            type_lst = g12d.get_tcker_type_lst(stocks_df)
            type_select = st.sidebar.multiselect('Type in the ticker type here', 
                                                options = type_lst,
                                                default = ["Common Stock"])   
                                                #default = ["Common", "Common Stock", "EQUITY"]) seems 12data removed the common and equity options
            # please add type_select value to a session state value 

            country_lst = g12d.get_tcker_country_lst(stocks_df)
            country_select = st.sidebar.multiselect('Type in the ticker country here', 
                                                    options = country_lst,
                                                    default = ["United States"])
            # please add country_select value to a session state value 

            exchange_lst = g12d.get_tcker_exchange_lst(stocks_df)
            exchange_select = st.sidebar.multiselect('Type in the ticker exchange here',
                                                    options = exchange_lst,
                                                    default = ["NASDAQ", "CBOE", "NYSE", "OTC"])
            # please add exchange_select value to a session state value 

            filter_submit = st.sidebar.button('Submit Filter Selection')
            if filter_submit:
                df_filter, symb_error_out_shre_lst, symb_error_flt_shre_lst = filterPrint(symbol_select, type_select, country_select, exchange_select )
                st.sidebar.markdown("---")
            # please add filter_submit value to a session state value

            msg = 'STOCK INTERVAL SELECTION'
            guiMrk.sideBarcolorHeader(fontcolor = '#800080', fontsze = 14, msg = msg)
            interval = st.sidebar.select_slider('Select Stock Data Interval',
                                    options=['1min', '5min', '15min', '30min', '45min', '1h', '2h', '4h', '1day', '1week', '1month'])
            st.sidebar.write(f'**Selected Stock Data Interval is {interval}**')
            st.sidebar.markdown("---")    
            # please add interval value to a session state value    

            msg = 'TIME RANGE SELECTION: START DATE'
            guiMrk.sideBarcolorMarkDown(fontcolor = '#800080', fontsze = 14, msg = msg)
            
            # assigning tuples to use
            approvedDateInputType = ('user provided StartDate', 'user provided EndDate')
            AllTimeRngeTuple = ('user provided StartDate', 'earliestTimeStamp','user provided EndDate', 'Time Interval', "Today's Date")

            startTimeRngeTuple = ('user provided StartDate', 'earliestTimeStamp', "Today's Date")
            startTimeRangeOption = st.sidebar.selectbox('Please select type of Start Date', startTimeRngeTuple )

            if startTimeRangeOption in approvedDateInputType:
                start_date_input = st.sidebar.date_input("Select Start Date", datetime.date(2022, 1, 1)) # FOR TESTING
                #start_date_input = st.sidebar.date_input("Select Start Date", datetime.date.today())
                st.sidebar.write('Start Date is:', start_date_input)

            elif startTimeRangeOption ==  "Today's Date":
                today_date_input = datetime.date.today()
                st.sidebar.write('Start Date is:', today_date_input)

            elif startTimeRangeOption ==  "earliestTimeStamp":
                st.sidebar.write(f'We will Calculate Start Date from {startTimeRangeOption}')
            st.sidebar.markdown("---")

            msg = 'TIME RANGE SELECTION: END DATE'
            guiMrk.sideBarcolorMarkDown(fontcolor = '#800080', fontsze = 14, msg = msg)
            EndTimeRngeTuple = guiLgc.getEndTimeRngeTuple(startTimeRangeOption)
            endTimeRangeOption = st.sidebar.selectbox('Please select type of End Date', EndTimeRngeTuple )

            if endTimeRangeOption in approvedDateInputType:
                end_date_input = st.sidebar.date_input("Select End Date", datetime.date.today())
                st.sidebar.write('End Date is:', end_date_input)

            elif endTimeRangeOption ==  "Today's Date":
                today_date_input = datetime.date.today()
                st.sidebar.write('End Date is:', datetime.date.today())

            elif endTimeRangeOption ==  "Time Interval":
                timeIntervalUnit = st.sidebar.selectbox('Please select Time Interval Unit?',('seconds', 'minutes', 'hours', 'days', 'weeks', 'months', 'years'))
                timeIntervalValue = st.sidebar.number_input('Insert a Time Interval Value', min_value = 1)
                st.sidebar.write(f'Selected Time Interval is {timeIntervalValue} {timeIntervalUnit}')

            else:
                st.sidebar.write(f'We will Calculate End Date from {endTimeRangeOption}')

            getTmeRnge = f'{startTimeRangeOption}-{endTimeRangeOption}'
        st.sidebar.markdown("---")
    button_submit = st.sidebar.button('Submit')
    if button_submit:
        pass
    






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









