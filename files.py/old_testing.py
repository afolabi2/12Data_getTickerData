# streamlit run ./files.py/old_testing.py

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import math


# programmatic calculations
import get12Data as g12d
import getAnalytics as gAna

def colorHeader(fontcolor = '#33ff33', fontsze = 30, msg="Enter some Text"):
    st.markdown(f'<h1 style="color:{fontcolor};font-size:{fontsze}px;">{msg}</h1>', unsafe_allow_html=True)

def analytics(df):
    df = addColumns(df)
    df = addVolatile(df)
    return df

def entryCond(s):
    if (s['Close'] > s['RollMax'] ):
        return 'YES'
    elif  (s['Close'] < s['RollMax'] ):
        return 'NO'
    else:
        return 'NEUTRAL'

def addColumns(df):
    new_df = df.copy(deep=True)

    new_df['RollMax'] = new_df['High'].rolling(13, min_periods=1).max().shift(1)
    new_df['RollMax'] = new_df['RollMax'].replace(np.nan, 0)
    

    # make sure type of data in columns are ok
    new_df['datetime'] = pd.to_datetime(df['datetime'])
    new_df["Open"] = pd.to_numeric(new_df["Open"])
    new_df["High"] = pd.to_numeric(new_df["High"])
    new_df["Low"] = pd.to_numeric(new_df["Low"])
    new_df["Close"] = pd.to_numeric(new_df["Close"])
    new_df["Volume"] = pd.to_numeric(new_df["Volume"])
    new_df["RollMax"] = pd.to_numeric(new_df["RollMax"])

    new_df["Entry"] = new_df.apply(entryCond, axis=1)
    return new_df

def addVolatile(df):
    Alength=0
    effectiveLen=math.ceil((Alength+1)/2)
    df['volatile']=df['High']+df['Low']+df['Close']+df['Open']
    df['volatile']=np.tan(df['volatile'].astype(float))
    df['volatile']= df['volatile'].round(2)

    conditions=[(df['volatile']==	122400.93),
                (df['volatile']==	13269.48),
                (df['volatile']==	54448.36),
                (df['volatile']==	17125.66),
                (df['volatile']==	7679.95),
                (df['volatile']==	6817.64),
                (df['volatile']==	5931.62),
                (df['volatile']==	5505.58),
                (df['volatile']==	4343.88),
                (df['volatile']==	2838.91),
                (df['volatile']==	2076.27),
                (df['volatile']==	1120.67),
                (df['volatile']==	946.3),
                (df['volatile']==	666.3),
                (df['volatile']==	599.51),
                (df['volatile']==	580.43),
                (df['volatile']==	514.16),
                (df['volatile']==	405.56),
                (df['volatile']==	418.59),
                (df['volatile']==	386.25),
                (df['volatile']==	377.88),
                (df['volatile']==	377.44),
                (df['volatile']==	294.43),
                (df['volatile']==	282.68),
                (df['volatile']==	264.43),
                (df['volatile']==	251.15),
                (df['volatile']==	231.1),
                (df['volatile']==	194.92),
                (df['volatile']==	192.56),
                (df['volatile']==	179.39),
                (df['volatile']==	176.23),
                (df['volatile']==	174.2),
                (df['volatile']==	174.08),
                (df['volatile']==	97.03),
                (df['volatile']==	80.71),
                (df['volatile']==	62.42),
                (df['volatile']==	58.25),
                (df['volatile']==	-56.77),
                (df['volatile']==	-71.52),
                (df['volatile']==	-131.39),
                (df['volatile']==	-135.33),
                (df['volatile']==	-154.74),
                (df['volatile']==	-166.16),
                (df['volatile']==	-190.94),
                (df['volatile']==	-207.22),
                (df['volatile']==	-225.95),
                (df['volatile']==	-305.14),
                (df['volatile']==	-496.67),
                (df['volatile']==	-702.21),
                (df['volatile']==	-806.19),
                (df['volatile']==	-808.01),
                (df['volatile']==	-981.97),
                (df['volatile']==	-1020.42),
                (df['volatile']==	-1555.67),
                (df['volatile']==	-1741.29),
                (df['volatile']==	-1766.62),
                (df['volatile']==	-1865.99),
                (df['volatile']==	-1929.14),
                (df['volatile']==	-3629.89),
                (df['volatile']==	-4600.91),
                (df['volatile']==	-8448.37),
                (df['volatile']==	-9645),
                (df['volatile']==	-13269.48),
                (df['volatile']==	-90747.27)]

    Value=["9.82-11.86",
            "222-217",
            "2.06-4.39-5.12|1.84-2.28",
            "36.53-39.9-27",
            "7.15-8.56",
            "219.69-223.55",
            "24.86-12.3|24.74-31.98",
            "1.96-1.9-2.12",
            "7.33-11.04",
            "5.1-1.5/9.4",
            "1.97-1.83-2.36",
            "0.39-2.29|0.33-4.85",
            "15-30.42|22.3",
            "10.6-14.7",
            "221-223-216",
            "8.72-6.12-9.27",
            "5.95-1.11|5.95-7/9/11",
            "33.5-44.5",
            "1.17-2.1/3.25|0.94-2.5",
            "1.17-1.44|1.65",
            "0.39-.35-.37",
            "16.5-11.66",
            ".39-.63",
            "6.59-9.18|6.65-6.95|6.68-5.75",
            "1.9-3.4",
            "2-.63-2.5|0.94-1.39-1.98|1.97-1.7-1.92",
            "57.56-164.58",
            "7.55-6.82-8.01",
            "42-53",
            "2.77-2.05-3.43o4.85",
            "2.62-3.84",
            "4.35-6.35",
            "283.79-277.8",
            "222.19-224.44",
            "1.18-0.33-1.83",
            "1.95-2.67",
            "3.57-2.89",
            "1.24-3.36",
            "2.01-1.6/1.95-1.18",
            "0.98-1.4-1.15-1.65-1.3-2|2.1-1.66-1.25-1.52-0.98",
            "2.01-2.74",
            "6.63-3.85-5.75-6.5-8.25-10.75-14.5",
            "2-2.51|1.78-2.18",
            "47.68-9.41-30",
            "2.75-1.5",
            "2.75-0.98/2.77-3.18o3.7o5.46",
            "9-8.94-2.8|8.27-11.24",
            "65.06-76.74",
            "23.9-28.37",
            "4.38-3.6-4.9",
            "518-498-538",
            "1.98-0.97/1.97-3",
            "19.68-10.64",
            "68-75",
            "2.76-1.54-1.8",
            "106.97-107.12",
            "14.5-9.9",
            "2.04-0.8-2.11",
            "29-34.3",
            "301-320.85",
            "1.97-2.31|1.96-1.76-2.03",
            "0.39-0.55",
            "221.92-216",
            "1.18-1.34"
            ]
    # numpy.select(condlist, choicelist, default=0)
    df['Range'] = np.select(conditions, Value, default = 0)
    
    df10 = df.loc[(df['volatile']==122400.93)|
                    (df['volatile']==13269.48)|
                    (df['volatile']==54448.36)|
                    (df['volatile']==17125.66)|
                    (df['volatile']==7679.95)|
                    (df['volatile']==6817.64)|
                    (df['volatile']==5931.62)|
                    (df['volatile']==5505.58)|
                    (df['volatile']==4343.88)|
                    (df['volatile']==2838.91)|
                    (df['volatile']==2076.27)|
                    (df['volatile']==1120.67)|
                    (df['volatile']==946.3)|
                    (df['volatile']==666.3)|
                    (df['volatile']==599.51)|
                    (df['volatile']==580.43)|
                    (df['volatile']==514.16)|
                    (df['volatile']==405.56)|
                    (df['volatile']==418.59)|
                    (df['volatile']==386.25)|
                    (df['volatile']==377.88)|
                    (df['volatile']==377.44)|
                    (df['volatile']==294.43)|
                    (df['volatile']==282.68)|
                    (df['volatile']==264.43)|
                    (df['volatile']==251.15)|
                    (df['volatile']==231.1)|
                    (df['volatile']==194.92)|
                    (df['volatile']==192.56)|
                    (df['volatile']==179.39)|
                    (df['volatile']==176.23)|
                    (df['volatile']==174.2)|
                    (df['volatile']==174.08)|
                    (df['volatile']==97.03)|
                    (df['volatile']==80.71)|
                    (df['volatile']==62.42)|
                    (df['volatile']==58.25)|
                    (df['volatile']==	-56.77)|
                    (df['volatile']==	-71.52)|
                    (df['volatile']==	-131.39)|
                    (df['volatile']==	-135.33)|
                    (df['volatile']==	-154.74)|
                    (df['volatile']==	-166.16)|
                    (df['volatile']==	-190.94)|
                    (df['volatile']==	-207.22)|
                    (df['volatile']==	-225.95)|
                    (df['volatile']==	-305.14)|
                    (df['volatile']==	-496.67)|
                    (df['volatile']==	-702.21)|
                    (df['volatile']==	-806.19)|
                    (df['volatile']==	-808.01)|
                    (df['volatile']==	-981.97)|
                    (df['volatile']==	-1020.42)|
                    (df['volatile']==	-1555.67)|
                    (df['volatile']==	-1741.29)|
                    (df['volatile']==	-1766.62)|
                    (df['volatile']==	-1865.99)|
                    (df['volatile']==	-1929.14)|
                    (df['volatile']==	-3629.89)|
                    (df['volatile']==	-4600.91)|
                    (df['volatile']==	-8448.37)|
                    (df['volatile']==	-9645)|
                    (df['volatile']==	-13269.48)|
                    (df['volatile']==	-90747.27)]

    df10.pop('Open')
    df10.pop('Close')
    #st.dataframe(df)
    return df

def df_getMinMaxVal_Column(df):
    minVal = df["Volume"].min()
    maxVal = df["Volume"].max()
    minVal = float(minVal)
    maxVal = float(maxVal)
    new_df = df.loc[lambda x: x.Volume >= minVal].loc[lambda x: x.Volume <= maxVal]
    return minVal, maxVal

def df_filter_Column(df, minVal, maxVal):
    new_df = df.loc[lambda x: x.Volume >= minVal].loc[lambda x: x.Volume <= maxVal]
    return new_df

if "getdf_expander" not in st.session_state: 
      st.session_state.getdf_expander = False  
if "moddf_expander" not in st.session_state: 
      st.session_state.moddf_expander = False 
if "filtdf_expander" not in st.session_state: 
      st.session_state.filtdf_expander = False 


st.session_state.getdf_expander = st.expander(f"get df")  
st.session_state.moddf_expander = st.expander(f"mod df")  
st.session_state.filtdf_expander = st.expander(f"filter df") 

msg_getdf = ''
with st.session_state.getdf_expander:
    tick = 'mitq'
    goog = yf.Ticker(f'{tick}')
    data = goog.history()
    data = data.reset_index() 
    data.columns = ['datetime', *data.columns[1:]]
 
    msg = f'getting data for'
    msg_getdf = msg_getdf + msg + '<br/>'
    msg = f'our ticker{tick}'
    msg_getdf = msg_getdf + msg + '<br/>'
    colorHeader(fontcolor = '#00008B', fontsze = 15, msg = msg_getdf)
    st.dataframe(data.head(10))

msg_moddf = ''
with st.session_state.moddf_expander:
    msg = f'modifying data for'
    msg_moddf = msg_moddf + msg + '<br/>'
    msg = f'our ticker{tick}'
    msg_moddf = msg_moddf + msg + '<br/>'
    colorHeader(fontcolor = '#00008B', fontsze = 15, msg = msg_moddf)
    trans_df = analytics(data)
    st.dataframe(trans_df.head(10))

with st.session_state.filtdf_expander:
    minVal, maxVal = df_getMinMaxVal_Column(trans_df)
    st.write(f'min value: {minVal} <br/> max value {maxVal}')
    volatile_slide = st.slider('Min and Max Volatile Column Range?', value = [minVal, maxVal])
    Voltle_df = df_filter_Column(trans_df, minVal, maxVal)
    st.dataframe(Voltle_df)
