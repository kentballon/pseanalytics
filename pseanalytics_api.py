#!/usr/bin/env python
#----------------------------------------------------------------------------
# investa_api.py
# 
# Module containing all common methods for pulling Stock data from
# https://www.investagrams.com/Stock
# 
# kentballon@gmail.com
# 
#----------------------------------------------------------------------------
import os
import pandas as pd
import numpy as np
from datetime import datetime

# defining the api-endpoint  
api_endpoint = "https://www.investagrams.com/Stock/"
# filters for data from web scrape
filters = ['<td class="table-info">','<td>','</td>','<td class="table-danger">','<td class="table-success">','<td,class="table-warning">','<td class="table-warning">','\r']

def post_fix_correction(string):
    retval = string
    if "M" in string:
        string = string.replace("M","")
        retval = float(string) * 1000000 
     
    if "K" in string:
        string = string.replace("K","")
        retval = float(string) * 1000

    if "%" in string:
        string = string.replace("%","")
        retval = string
    return retval

def get_rsi(data, time_window):
    # reference: https://tcoil.info/compute-rsi-for-stocks-with-python-relative-strength-index/
    diff = data.diff(1).dropna()        # diff in one field(one day)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff
    
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]
    
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]
    
    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi

def get_stock_data(stock,start_date="2020-01-02",end_date="2020-01-02"):

    # get all stock data available
    command = "curl -s " + api_endpoint + stock + " | grep table-info | awk -F 'table-info\">' '{print $2}'"
    stream = os.popen(command)
    output = stream.read()

    # remove filter words
    for f in filters:
        if (f == "</td>"):
          output = output.replace(f,"|")
        else:
          output = output.replace(f,"")

    outputarr = output.split('\n')

    # prepare dataframe input
    data = []
    for entry in outputarr:
        if not entry == "" :
            list_entry = entry.split("|")[:-1]
            dt_string = list_entry[0]
            # format date
            list_entry[0] = datetime.strptime(dt_string, "%b %d, %Y")
            # format pchange 
            list_entry[3] = post_fix_correction(list_entry[3])
            # format volume
            list_entry[7] = post_fix_correction(list_entry[7])
            # format netforeign
            list_entry[8] = post_fix_correction(list_entry[8])
            data.insert(0,list_entry)
    
    # create dataframe
    df = pd.DataFrame(data, columns=['date','close','change','pchange','open','low','high','volume','netforeign'])

    # format all columns as float except for date
    for col in df.columns:
        if not (col== "date"):
            df[col] = df[col].astype(float)

    # set date as search index
    df = df.set_index(['date'])

    # calculate EMA
    df['9ema'] = df.iloc[:,0].ewm(span=9,adjust=False).mean()
    df['12ema'] = df.iloc[:,0].ewm(span=12,adjust=False).mean()
    df['20ema'] = df.iloc[:,0].ewm(span=20,adjust=False).mean()
    df['26ema'] = df.iloc[:,0].ewm(span=26,adjust=False).mean()
    df['50ema'] = df.iloc[:,0].ewm(span=50,adjust=False).mean()
    df['100ema'] = df.iloc[:,0].ewm(span=100,adjust=False).mean()
    
    # calculate MACD
    df['macd'] = df['12ema'] - df['26ema']
    df['macd_signal'] = df.iloc[:,14].ewm(span=9,adjust=False).mean()

    # calculate RSI
    df['rsi'] = get_rsi(df['close'],14)
 
    # limit dataframe to date range
    retdf = df.loc[start_date:end_date]
    # reset the index
    retdf = retdf.reset_index()
    # sort by date
    retdf.sort_values(by=['date'], inplace=True, ascending=True)

    return retdf 
