#!/usr/bin/env python

import sys
import pandas as pd
from datetime import date, timedelta
from pseanalytics import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

report_date = date.today()

if (len(sys.argv) > 2):
    csv_file_name = sys.argv[2]
    report_date = sys.argv[1]
elif (len(sys.argv) > 1):
    csv_file_name = 'lists/code_list_test.txt'
    report_date = sys.argv[1]
else:
    csv_file_name = 'lists/code_list_test.txt'
    report_date = report_date.strftime("%Y-%m-%d")

res = strategies.rsi_overbought(csv_file_name,report_date,trendfac=1)
df = res.get_stock_data()

print df
