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
filters = ['<td class="table-info">','<td>','</td>','<td class="table-danger">','<td class="table-success">','<td,class="table-warning">','<td class="table-warning">','\r']

def post_fix_correction(string):
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
            list_entry = entry.split("|")
            list_entry = list_entry[:-1]
            dt_string = list_entry[0]
            list_entry[0] = datetime.strptime(dt_string, "%b %d, %Y")
            list_entry[3] = post_fix_correction(list_entry[3])
            list_entry[7] = post_fix_correction(list_entry[7])
            list_entry[8] = post_fix_correction(list_entry[8])
            data.append(list_entry)

    # create dataframe
    df = pandas.DataFrame(data, columns=['date','lastprice','change','pchange','open','low','high','volume','netforeign'])

    df = df.set_index(['date'])
    return df.loc[end_date:start_date]
