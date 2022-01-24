import streamlit as st
from io import StringIO 

def readFileasStr(uploaded_file):
# To read file as string:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    tcker_lst = g12d.get_tcker_lst_fromStringIO(string_data)

    illegal_tcker = list(set(tcker_lst) - set(stocks_df.symbol))
    legal_tcker   = list(set(tcker_lst) - set(illegal_tcker))

    return illegal_tcker, legal_tcker

def getEndTimeRngeTuple(startTimeRangeOption):
    EndTimeRngeTuple = ('earliestTimeStamp','user provided StartDate', 'user provided EndDate', 'Time Interval', "Today's Date" )
    if startTimeRangeOption == 'earliestTimeStamp':
        EndTimeRngeTuple = ('user provided EndDate', 'Time Interval', "Today's Date")
    elif startTimeRangeOption == 'user provided StartDate':
        EndTimeRngeTuple = ('user provided EndDate', 'Time Interval', "Today's Date")
    #elif startTimeRangeOption == 'user provided EndDate':
    #    EndTimeRngeTuple = ('earliestTimeStamp', 'user provided StartDate', 'Time Interval', "Today's Date")
    #elif startTimeRangeOption == 'Time Interval':
    #    EndTimeRngeTuple = ('earliestTimeStamp', 'user provided StartDate', 'user provided EndDate', "Today's Date")
    elif startTimeRangeOption == "Today's Date":
        EndTimeRngeTuple = ("Time Interval",  "Today's Date")
    return EndTimeRngeTuple
