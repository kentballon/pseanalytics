#!/usr/bin/env python

import sys
import time
import pandas as pd
import argparse
import yagmail
from datetime import date, timedelta
from pseanalytics import *
username = "USERNAME@DOMAIN.COM"
password = "PASSWORD"
delay = 300

def init_test():

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    report_date = date.today()
    
    # create parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="Report date", default=report_date.strftime("%Y-%m-%d"))
    parser.add_argument("-l", help="Stock code list", default="../lists/code_list_watcher.txt")
    parser.add_argument("-s", help="Samples to evaulate", type=int, default=0)

    # parse arguments
    args = parser.parse_args()
    return args

args = init_test()

while True:
    res = strategies.marketsummary(args.l,args.d,args.s)
    df = res.get_stock_data()
    
    watchlist = pd.read_csv(args.l)
    min_breached = {}
    max_breached = {}
    for ind in watchlist.index:
            stock = watchlist['stock'][ind]
            check = df.loc[df['stock'] == stock]
            if watchlist['min'][ind] is not None:
                if (check['close'][0] <= watchlist['min'][ind]):
                    min_breached.update({stock:[check['close'][0],watchlist['min'][ind]]})
            if watchlist['max'][ind] is not None:
                if (check['close'][0] >= watchlist['max'][ind]):
                    max_breached.update({stock:[check['close'][0],watchlist['max'][ind]]})
    
    contents = [
        "Minimum threshold breached:\n",
        str(min_breached),
        "Maximum threshold breached:\n",
        str(max_breached)
    ]
    
    yagmail.SMTP(username,password).send('kentballon@gmail.com', 'pseanalytics watcher', contents)
    time.sleep(delay)
