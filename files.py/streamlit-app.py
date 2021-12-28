import streamlit as st

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

#DataSource Radio Buttons
# inst_type will be stored
inst_lst   = ["Stock Ticker", "(Not Ready)Crypto Currency"]
inst_radio = st.radio("Please select an Instrument Type", inst_lst)
st.write(f"**{inst_radio} Data selected**")
st.markdown("---")

if inst_radio == "Stock Ticker":
    #DataSource Radio Buttons
    #data_src will be stored
    datasrc_lst = ["12 Data", "(Not Ready)Alpha-Vantage", "(Not Ready)Alpaca"]
    src_radio = st.radio("Stock Data API", datasrc_lst) 
    st.write(f"**{src_radio} API selected**")
    st.markdown("---")

    ApiKey_lst = ["Default", "Enter API Key", "(Not Ready)Use Envir Stored Variable '12DataApiKey'", "(Not Ready)Get api from file"]
    ApiKey_radio = st.radio("Please select an Instrument Type", ApiKey_lst)
    
    if ApiKey_radio == "Default":
        st.write(f'{ApiKey_radio} 12Data ApiKey will be used')
        apikey_12Data = "7940a5c7698545e98f6617f235dd1d5d"
    elif ApiKey_radio == "Enter API Key":
        apikey_12Data = st.text_input('Please Enter 12 Data API Key', 'Please Enter 12 Data API Key')
        
    

    
