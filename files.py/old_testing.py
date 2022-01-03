import pandas as pd 
import json
import getYfData as yfd

# to run streamlit app
# streamlit run ./files.py/old_testing.py


print("starting")

symbol = "AACOU"
#symbol = "TSLA"
x,y = yfd.get_yf_float_outstand_shares(symbol)
print(x,y)

print("ending")

#primaryColor="#0de69e"