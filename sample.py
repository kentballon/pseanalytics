#!/usr/bin/env python

import pseanalytics_api 
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

stockID="MPI"
data = pseanalytics_api.get_stock_data(stockID,"2019-06-11","2020-06-11")
data = data.round(2)
print data
