import pseanalytics_api 
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

stockID="FRUIT"
data = pseanalytics_api.get_stock_data(stockID,"2020-05-01","2020-06-12")
print data
