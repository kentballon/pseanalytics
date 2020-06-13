#!/usr/bin/env python

import sys
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
    start_date = report_date - timedelta(days=365)

    # create parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="Report date", default=report_date.strftime("%Y-%m-%d"))
    parser.add_argument("-s", help="Start date", default=start_date.strftime("%Y-%m-%d"))
    parser.add_argument("-c", help="Stock code", default="MPI")
    # parse arguments
    args = parser.parse_args()
    return args

args = init_test()
data = pseanalytics.get_stock_data(args.c,args.s,args.d)
data = data.round(2)

print data
