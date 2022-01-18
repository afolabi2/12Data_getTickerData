import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import json
import pandas as pd
import numpy as np
import pathlib
import streamlit as st
import getYfData as yfd
from time import sleep
import time
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta, MO
import math

from dataclasses import dataclass
from dataclasses import field
from dataclasses import InitVar

import get12Data as g12d
from time import sleep
import streamlit as st
# to run streamlit app
# streamlit run ./files.py/testing2.py


demo_apikey_12Data = "7940a5c7698545e98f6617f235dd1d5d"
twelvedata_api_key: str = "69287070d2f24f60a821b96ec1281011"
msg_all = ''
symbol = 'AAPL'
start = '2022-01-10 09:00:00'
end = '2022-01-13 12:00:00'
interval = '2h'


twelvedata_url = f'https://api.twelvedata.com/time_series?&symbol={symbol}&start_date={start}&end_date={end}&interval={interval}&apikey={twelvedata_api_key}'


session = requests.Session()
# In case I run into issues, retry my connection
retries = Retry(total=5, backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))
# Initial request to get the ticker count
r = session.get(twelvedata_url)
json_object = r.json()
#st.write(json_object)
value_data = json_object['values']
print('')
df = pd.DataFrame(value_data)
print(df.head(5))
print(df.tail(5))
