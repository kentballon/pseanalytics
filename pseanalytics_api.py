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
import pandas
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
    df = pandas.DataFrame(data, columns=['date','close','change','pchange','open','low','high','volume','netforeign'])
    # set date as search index
    df = df.set_index(['date'])
    # limit dataframe to date range
    #retdf = df.loc[end_date:start_date]
    retdf = df.loc[start_date:end_date]
    # reset the index
    retdf = retdf.reset_index()
    # sort by date
    retdf.sort_values(by=['date'], inplace=True, ascending=True)

    return retdf 
