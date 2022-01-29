import streamlit as st
import pandas as pd
import datetime
from io import StringIO 

from dataclasses import dataclass
from dataclasses import field
from dataclasses import InitVar

import os

# gui helper functions
import guiMarkDown as guiMrk #used for markdown and write functions

# gui
import guiSidebar as guiSide
import guiMainArea as guiMain

# programmatic calculations
import get12Data as g12d
import getAnalytics as gAna


# ====================
# RUN APP!!!!!
# ====================
# to run streamlit app
# streamlit run ./files.py/streamlit-app.py

#mitq and gree brtx gfai need testing
#utme atvi working


# ====================
# WAITING TASKS
# ====================
# Need to comment every line/action done!!!!!!!

# ====================
# FIRST SETTINGS FUNCTIONS
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

# ====================
# SETTINGS FUNCTIONS
# ====================
def initPageSettings():
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
# PRINT OUT FUNCTIONS
# ====================
def setDfFormat():
    # ====================
    # DATAFRAME FORMATTING 
    # ====================
    pd.options.display.float_format = '{:,}'.format

# get dataframe of lists of Stock Dataframe
@st.cache
def initTickerLst(apikey_12Data):
    stocks_df = g12d.get_tck_stocks_df(apikey_12Data)
    return stocks_df

# Set Demo and paid Keys for 12Data API keys
def setDemoApiKey():
    Data12_DemoKey = "7940a5c7698545e98f6617f235dd1d5d"
    os.environ['Data12_DemoKey'] = str(Data12_DemoKey)

def setPaidApiKey():
    Data12_PaidKey = "69287070d2f24f60a821b96ec1281011"
    os.environ['Data12_PaidKey'] = str(Data12_PaidKey)

def getDemoApiKey():
    Data12_DemoKey = os.environ.get('Data12_DemoKey', 'Not Set')
    if Data12_DemoKey != 'Not Set':
            return Data12_DemoKey
    else:
        raise ValueError('Computer does not hold a demo apikey env. variable .')
        st.write('wahala dey')
        setDemoApiKey()
        getDemoApiKey()

def getPaidApiKey():
    Data12_PaidKey = os.environ.get('Data12_PaidKey', 'Not Set')
    if Data12_PaidKey != 'Not Set':
            return Data12_PaidKey
    else:
        raise ValueError('Computer does not hold a paid apikey env. variable .')
        setPaidApiKey()
        getPaidApiKey()
    
def initSessionStates():
    if "df_stock" not in st.session_state:      
        st.session_state.df_stock = pd.DataFrame()  
    if "Data12_PaidKey" not in st.session_state:      
        st.session_state.Data12_PaidKey = '' 
    if "Data12_DemoKey" not in st.session_state:      
        st.session_state.Data12_DemoKey = ''
    
    #if "messages" not in st.session_state:      
    #    st.session_state.messages = []    
    #if "dataframe" not in st.session_state: 
    #    st.session_state.df_filter = []   
    #if "df_use12Data" not in st.session_state: 
    #    st.session_state.df_use12Data = []  
    #if "symb_lst" not in st.session_state: 
    #    st.session_state.symb_lst = []  
    #if "df_12TSD" not in st.session_state: 
    #    st.session_state.df_12TSD = []

def initSessionApiKeys(Data12_PaidKey,Data12_DemoKey):
    st.session_state.Data12_PaidKey = Data12_PaidKey
    st.session_state.Data12_DemoKey = Data12_DemoKey


def initStockDf(Data12_PaidKey):
    st.session_state.df_stock = initTickerLst(Data12_PaidKey)

def initAllSettings():
    #initialise required page settings
    initPageSettings()
    
    #initialise session states variables to use
    initSessionStates()

    #set format type of df's
    setDfFormat()

    # get 12data api keys
    Data12_DemoKey = getDemoApiKey()
    Data12_PaidKey = getPaidApiKey()
    
    initSessionApiKeys(Data12_PaidKey,Data12_DemoKey)
    initStockDf(st.session_state.Data12_PaidKey)

def showGui():
    initAllSettings()
    
    guiSide.sideGui()

    guiMain.get12main()
    guiMain.use12main()
    guiMain.get12TSDmain()
    guiMain.get12Analytics()

if __name__ == "__main__":
   showGui()
