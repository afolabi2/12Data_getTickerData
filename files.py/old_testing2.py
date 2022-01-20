import streamlit as st
import pandas as pd
import datetime
from io import StringIO 

from dataclasses import dataclass
from dataclasses import field
from dataclasses import InitVar

import get12Data as g12d
import getAnalytics as gAna
# ====================
# RUN APP!!!!!
# ====================
# to run streamlit app
# streamlit run ./files.py/old_testing2.py

# ---- Modules ------- 
import plotly.express as px

st.header("Fruits List")
# ---- Creating Dictionary ----
_dic = { 'Name': ['Mango', 'Apple', 'Banana'],
         'Quantity': [45, 38, 90]}
load = st.button('Load Data')
if load:
    _df = pd.DataFrame(_dic)
    st.write(_df)
   
   # ---- Plot types -------
    opt = st.radio('Plot type :',['Bar', 'Pie'])
    if opt == 'Bar':
        fig = px.bar(_df, x= 'Name', y = 'Quantity',title ='Bar Chart')
        st.plotly_chart(fig)
   
    else:     
      fig = px.pie(_df,names = 'Name', values = 'Quantity',title ='Pie Chart')
      st.plotly_chart(fig)