#!/usr/bin/env python
# ------------------------------------------------------------------------------------------------------
# strategies.py
#
# Collection of methods implementing trading strategies based on specified 
# criteria and identifies potential trades
# 
# kentballon@gmail.com
#
# ------------------------------------------------------------------------------------------------------
import pandas as pd
import sys
import pseanalytics_api as pseapi
from datetime import date, timedelta

# ------------------------------------------------------------------------------------------------------
# Configuration Parameters
# ------------------------------------------------------------------------------------------------------
# number of days to sample for the trend 
gtrendfac = 3
# adjust head factor relative to body 
gresfac = 1
# adjust tail factor relative to body 
gsupfac = 1
# percent change to consider 
gpc_fac = 0
# trade volume targets
gvolfac_1 =  1000000
gvolfac_2 =  5000000
gvolfac_3 = 10000000
# net foreign factor
gnetffac = 0
# ------------------------------------------------------------------------------------------------------
# result criteria
gpc_crit = 2
gvolfac_crit = (gvolfac_1 + gvolfac_2 + gvolfac_1)/(gvolfac_1)
gres_crit = 0
gsup_crit = 0
# ------------------------------------------------------------------------------------------------------

def get_whitesoldier_score(df, keys,trendfac,resfac,supfac,pc_fac,volfac_1,volfac_2,volfac_3,netffac,pc_crit,volfac_crit,res_crit,sup_crit):
  # create dataframe for overall tally
  df_score = pd.DataFrame(columns=['stock', 'volume_score', 'pchange_score','resistance_score','support_score','net_foreign_score'])
  for key in keys:
    volume_score = 0
    pchange_score = 0
    support_score = 0
    resistance_score = 0
    net_foreign_score = 0

    df_subset = df[df.stock == key]
    df_subset = df_subset.tail(int(trendfac))
    for ind in df_subset.index:

      # compute volume criteria
      if (df_subset['volume'][ind] >= volfac_3):
        volume_score = volume_score + 3
      elif (df_subset['volume'][ind] >= volfac_2):
        volume_score = volume_score + 2
      elif (df_subset['volume'][ind] >= volfac_1):
        volume_score = volume_score + 1
      else:
        volume_score = volume_score - 2

      # compute percent change criteria
      if (df_subset['pchange'][ind] > pc_fac):
        pchange_score = pchange_score + 1
      #else:
      #  pchange_score = pchange_score - 1

      # compute resistance criteria
      if (df_subset['pchange'][ind] > 0):
        if (df_subset['closeh'][ind] >= (resfac * df_subset['body'][ind])):
          resistance_score = resistance_score + 1
        #else:
        #  resistance_score = resistance_score - 1
      else:
        if (df_subset['openh'][ind] >= (resfac * df_subset['body'][ind])):
          resistance_score = resistance_score + 1
        #else:
        #  resistance_score = resistance_score - 1

      # compute support criteria
      if (df_subset['pchange'][ind] > 0):
        if (df_subset['opent'][ind] >= (supfac * df_subset['body'][ind])):
          support_score = support_score + 1
        #else:
        #  support_score = support_score - 1
      else:
        if (df_subset['closet'][ind] >= (supfac * df_subset['body'][ind])):
          support_score = support_score + 1
        #else:
        #  support_score = support_score - 1

      # compute percent change criteria
      if (df_subset['netforeign'][ind] > netffac):
        net_foreign_score = net_foreign_score + 1
      #else:
      #  net_foreign_score = net_foreign_score - 1
 
    # check overall condition
    if (volume_score >= volfac_crit 
        and pchange_score >= pc_crit
        and resistance_score >= res_crit 
        and support_score >= sup_crit 
       ):
      df_score = df_score.append({'stock': key, 
                                  'volume_score': volume_score, 
                                  'pchange_score': pchange_score, 
                                  'resistance_score': resistance_score, 
                                  'support_score': support_score, 
                                  'net_foreign_score': net_foreign_score}, 
                                  ignore_index=True)
  return df_score
    
def get_whitesoldier_stocks(df, keys,trendfac):
  for key in keys:
    df_subset = df[df.stock == key]
    df_subset = df_subset.tail(int(trendfac))
    #df_subset = df_subset.sort_values(by=['date'])
    print df_subset

def whitesoldiers(csv_file_name,trendfac=gtrendfac,resfac=gresfac,supfac=gsupfac,pc_fac=gpc_fac,volfac_1=gvolfac_1,volfac_2=gvolfac_2,volfac_3=gvolfac_3,netffac=gnetffac,pc_crit=gpc_crit,volfac_crit=gvolfac_crit,res_crit=gres_crit,sup_crit=gsup_crit):
    df = pd.read_csv(csv_file_name)
    report_date= date.today()
    report_date_n_days_ago = report_date - timedelta(days=trendfac)
    report_date = report_date.strftime("%Y-%m-%d")
    report_date_n_days_ago = report_date_n_days_ago.strftime("%Y-%m-%d")
    cnt = 0
    for stock in df['stock']:
        data = pseapi.get_stock_data(stock,report_date_n_days_ago,report_date)
        data = data.round(2)
    
        if cnt == 0:
            fulldata = data
            cnt = 1
        else:
            fulldata = fulldata.append(data,ignore_index = True)
    
    keys = pseapi.get_uniq_stock_keys(fulldata)
    filtered_df_score = get_whitesoldier_score(fulldata, keys,trendfac,resfac,supfac,pc_fac,volfac_1,volfac_2,volfac_3,netffac,pc_crit,volfac_crit,res_crit,sup_crit)
    filtered_keys = pseapi.get_uniq_stock_keys(filtered_df_score)
    filtered_df = get_whitesoldier_stocks(fulldata,filtered_keys,trendfac)

    return filtered_df, filtered_df_score
