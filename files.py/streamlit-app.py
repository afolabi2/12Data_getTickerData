import streamlit as st
import datetime

# to run streamlit app
# streamlit run ./files.py/streamlit-app.py

#Text Title
author = 'akt'
version = '0.001'
title_01 = f'Pull Stock Data App(Streamlit)'
st.title(title_01)

#Text Header/SubHeader
header_01    = f'by {author}'
subheader_01 = f'@version{version}'
st.header(header_01)
st.subheader(subheader_01)
st.markdown("---")
st.markdown("### WAITING TASKS")
st.markdown('> 1. Ticker listing has not been added yet o')
st.markdown("---")
#DataSource Radio Buttons
# inst_type will be stored
st.markdown("### INSTRUMENT SELECTION")
inst_lst   = ["Stock Ticker", "(Not Ready)Crypto Currency"]
inst_radio = st.radio("Please select an Instrument Type", inst_lst)
st.write(f"**{inst_radio} Data selected**")
st.markdown("---")

if inst_radio == "Stock Ticker":
    #DataSource Radio Buttons
    #data_src will be stored
    st.markdown("### DATA SOURCE SELECTION")
    datasrc_lst = ["12 Data", "(Not Ready)Alpha-Vantage", "(Not Ready)Alpaca"]
    src_radio = st.radio("Stock Data API", datasrc_lst) 
    st.write(f"**{src_radio} API selected**")
    st.markdown("---")

    if src_radio == "12 Data":
        st.markdown("### API KEY INPUT")
        ApiKey_lst = ["Default", "Enter API Key", "(Not Ready)Use Envir Stored Variable '12DataApiKey'", "(Not Ready)Get api from file"]
        ApiKey_radio = st.radio("Please provide API Key", ApiKey_lst)

            
    
        if ApiKey_radio == "Default":
            st.write(f'{ApiKey_radio} 12Data ApiKey will be used')
            apikey_12Data = "7940a5c7698545e98f6617f235dd1d5d"
        elif ApiKey_radio == "Enter API Key":
            apikey_12Data = st.text_input('Please Enter 12 Data API Key', 'Please Enter 12 Data API Key')
        st.markdown("---")
        
        st.markdown("### STOCK INTERVAL SELECTION")
        interval = st.select_slider('Select Stock Data Interval',
                                options=['1min', '5min', '15min', '30min', '45min', '1h', '2h', '4h', '1day', '1week', '1month'])
        st.write(f'Selected Stock Data Interval is {interval}')
        st.markdown("---")

        #st.markdown("### TIME RANGE SELECTION")
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

        st.markdown("### TIME RANGE SELECTION")
        approvedDateInputType = ('user provided StartDate', 'user provided EndDate', "Today's Date")

        col1, col2 = st.columns(2)
        with col1:
            startTimeRngeTuple = ('earliestTimeStamp','user provided StartDate', 'user provided EndDate', 'Time Interval', "Today's Date")
            st.header("Start Type")
            startTimeRangeOption = st.selectbox('Please select type of Start Date', startTimeRngeTuple )

            if startTimeRangeOption in approvedDateInputType:
                start_date_input = st.date_input("Select Start Date", datetime.date.today())
                st.write('Start Date is:', start_date_input)

        with col2:
            EndTimeRngeTuple = ('earliestTimeStamp','user provided StartDate', 'user provided EndDate', 'Time Interval', "Today's Date", )
            if startTimeRangeOption == 'earliestTimeStamp':
                EndTimeRngeTuple = ('user provided StartDate', 'user provided EndDate', 'Time Interval', "Today's Date")
            elif startTimeRangeOption == 'user provided StartDate':
                EndTimeRngeTuple = ('earliestTimeStamp', 'user provided EndDate', 'Time Interval', "Today's Date")
            elif startTimeRangeOption == 'user provided EndDate':
                EndTimeRngeTuple = ('earliestTimeStamp', 'user provided StartDate', 'Time Interval', "Today's Date")
            elif startTimeRangeOption == 'Time Interval':
                EndTimeRngeTuple = ('earliestTimeStamp', 'user provided StartDate', 'user provided EndDate', "Today's Date")
            elif startTimeRangeOption == "Today's Date":
                EndTimeRngeTuple = ('earliestTimeStamp', 'user provided StartDate', 'user provided EndDate', "Time Interval")
            
            st.header("End Type")
            endTimeRangeOption = st.selectbox('Please select type of End Date', EndTimeRngeTuple )

            if endTimeRangeOption in approvedDateInputType:
                end_date_input = st.date_input("Select End Date", datetime.date.today())
                st.write('End Date is:', end_date_input)
        

            



        
    

    
