#!/usr/bin/env python

import pandas as pd
import argparse
from datetime import date, timedelta
from pseanalytics import *

def init_test():

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    report_date = date.today()

    # create parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="Report date", default=report_date.strftime("%Y-%m-%d"))
    parser.add_argument("-l", help="Stock code list", default="lists/code_list_test.txt")
    parser.add_argument("-s", help="Samples to evaulate", type=int, default=1)

    # parse arguments
    args = parser.parse_args()
    return args

args = init_test()
res = strategies.rsi_oversold(args.l,args.d,args.s)
df = res.get_stock_data()

print df
