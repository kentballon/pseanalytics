#!/usr/bin/env python

import pandas as pd
from pseanalytics import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

if (len(sys.argv) > 1):
    stockID= sys.argv[1]
else:
    stockID="MPI"

data = pseanalytics.get_stock_data(stockID,"2019-06-11","2020-06-11")
data = data.round(2)
print data
