import streamlit as st
import datetime
import get12Data as g12d
import pandas as pd 
import json

# to run streamlit app
# streamlit run ./files.py/old_testing.py

symbol = 'AAPL'
apikey_12Data = "7940a5c7698545e98f6617f235dd1d5d"
shit_df = g12d.get_tck_lst_df(apikey_12Data)
kill = st.dataframe(shit_df)

type_filter = []
country_filter = []
exchange_filter = []


type_filter = st.multiselect(
    "Filter By Type",
    options = sorted(shit_df["type"].unique()),
    default = ["Common", "Common Stock", "EQUITY"])


country_filter = st.multiselect(
    "Filter By Country",
    options = sorted(shit_df["country"].unique()),
    default = ["United States"])

exchange_filter = st.multiselect(
    "Filter By Exchange",
    options = sorted(shit_df["exchange"].unique()))
    #default = sorted(shit_df["exchange"].unique()))


print(type_filter)