#!/usr/bin/env python

import sys
import pseanalytics_api as pseapi 
import strategies
import pandas as pd
from datetime import date, timedelta

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

if (len(sys.argv) > 1):
    csv_file_name = sys.argv[1]
else:
    csv_file_name = 'lists/code_list_test.txt'

df, score = strategies.whitesoldiers(csv_file_name)

print df
print score
