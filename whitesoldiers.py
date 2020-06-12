#!/usr/bin/env python

import sys
import pandas as pd
from datetime import date, timedelta
from pseanalytics import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

if (len(sys.argv) > 1):
    csv_file_name = sys.argv[1]
else:
    csv_file_name = 'lists/code_list_test.txt'

ws = strategies.whitesoldier(csv_file_name,report_date='2020-06-11',trendfac=4)
df, score = ws.get_stock_data()

print df
print score
