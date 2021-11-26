# region IMPORTS
import datetime
from datetime import timedelta
import os
from os.path import exists

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
from matplotlib import dates as mdates

import logging
import roles


# endregion

# region ENVIRONMENT
logging.basicConfig(filename="/tmp/sync-reportgen-type6.log", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")
logging.info(f"********************** STARTING REPORT GEN - FULL SUMMARY With Period Summary")
print("Starting Report Gen...")
# endregion

# region VARIABLES
x = datetime.datetime.now()
y = x - timedelta(days=1)
today = x.strftime("%Y%m%d")
logging.info(f"Runtime: {today}")
yesterday = y.strftime("%Y%m%d")

# PATHS
rawpath = "/var/www/html/RankData"
reportout = "/var/www/html/reports"


# GENERATE FOLDER LISTS
print("Checking Folder Paths...")

runtimes = os.listdir(rawpath)
runtimes = sorted(runtimes, reverse=True)
#print(runtimes)
logging.info(f"Crawl Runtimes: {runtimes}")

# DATASETS
crit = ['win','use','ban']
period = ["day1","day30","day60","day90","day180","day365"]
level = ["All", "Legend", "Mythic"]
prof = ["assassin","marksman","mage","tank","support","fighter"]

# endregion

# region CHECK PATHS
# Generate Folders
if not os.path.exists(reportout):
    os.system(f"mkdir {reportout}")
    print(f"Making Folder: {reportout}")
    logging.info(f"Making Folder: {reportout}")

# endregion

# region TABLE GEN
print("Compiling Lookups...")
logging.info("Compiling Lookups")

# Create master table
runtimes = sorted(runtimes, reverse=True)
runtime = runtimes[0]
dfs = pd.DataFrame(columns=['name','elo'])
# START THE CRAWLER

for tp in period:
    if tp == "day1":
        d = 1
        dt = "Day"
    elif tp == "day30":
        d = 30
        dt = "Month"
    elif tp == "day60":
        d = 60
        dt = "BiMonth"
    elif tp == "day90":
        d = 90
        dt = "Season"
    elif tp == "day180":
        d = 180
        dt = "SemiAnnual"
    elif tp == "day365":
        d = 365
        dt = "Year"

    print(f"Running: {dt}:{tp}")
    from functions import statstable
    dfx = statstable(d, rawpath)

    #print(dfx)


    # TEST OUT TO CSV
    #print(f"Source Table... \n{dfx}")
    #dfx.to_csv(f"{reportout}/csv/rd.{dt}.master.csv",index=False)
    #print(f"Combined CSV: {reportout}/rd.{dt}.master.csv")
    #input("Press Enter to continue...")

    # Calculate Averages
    if tp == "day1":
        dfs['name'] = dfx['name'].values
        dfs['elo'] = dfx['elo'].values
        print(dfs)
    elif tp == "day30":
        dfm = dfx.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(win_m=lambda gdf: gdf['win'].mean()))
        dfm = dfm.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(use_m=lambda gdf: gdf['use'].mean()))
        dfm = dfm.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(ban_m=lambda gdf: gdf['ban'].mean()))
        dfm = dfm[dfm['runtime'] == runtime]
        dfm = dfm[['name', 'win_m', 'use_m', 'ban_m', 'elo']]
        print(dfm)
        dfs = pd.merge(dfs, dfm, how='inner', on=['name', 'elo'])
        print(dfs)
    elif tp == "day60":
        dfb = dfx.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(win_b=lambda gdf: gdf['win'].mean()))
        dfb = dfb.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(use_b=lambda gdf: gdf['use'].mean()))
        dfb = dfb.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(ban_b=lambda gdf: gdf['ban'].mean()))
        dfb = dfb[dfb['runtime'] == runtime]
        dfb = dfb[['name', 'win_b', 'use_b', 'ban_b', 'elo']]
        print(dfb)
        dfs = pd.merge(dfs, dfb, how='inner', on=['name', 'elo'])
        print(dfs)
    elif tp == "day90":
        df3 = dfx.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(win_s=lambda gdf: gdf['win'].mean()))
        df3 = df3.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(use_s=lambda gdf: gdf['use'].mean()))
        df3 = df3.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(ban_s=lambda gdf: gdf['ban'].mean()))
        df3 = df3[df3['runtime'] == runtime]
        df3 = df3[['name', 'win_s', 'use_s', 'ban_s', 'elo']]
        print(df3)
        dfs = pd.merge(dfs, df3, how='inner', on=['name', 'elo'])
        print(dfs)
    elif tp == "day180":
        dfa = dfx.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(win_a=lambda gdf: gdf['win'].mean()))
        dfa = dfa.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(use_a=lambda gdf: gdf['use'].mean()))
        dfa = dfa.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(ban_a=lambda gdf: gdf['ban'].mean()))
        dfa = dfa[dfa['runtime'] == runtime]
        dfa = dfa[['name', 'win_a', 'use_a', 'ban_a', 'elo']]
        print(dfa)
        dfs = pd.merge(dfs, dfa, how='inner', on=['name', 'elo'])
        print(dfs)
    elif tp == "day365":
        dfy = dfx.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(win_y=lambda gdf: gdf['win'].mean()))
        dfy = dfy.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(use_y=lambda gdf: gdf['use'].mean()))
        dfy = dfy.groupby(['name', 'elo'], as_index=False).apply(lambda gdf: gdf.assign(ban_y=lambda gdf: gdf['ban'].mean()))
        dfy = dfy[dfy['runtime'] == runtime]
        dfy = dfy[['name', 'win_y', 'use_y', 'ban_y', 'elo']]
        print(dfy)
        dfs = pd.merge(dfs, dfy, how='inner', on=['name', 'elo'])
        print(dfs)

print(dfs)
dfs = dfs.round(2)

# ROLE
for p in prof:
    # print(f"Matching {p}:")
    rslt = getattr(roles, p)
    dfs.loc[dfs.name.isin(rslt), 'role'] = p

dfs.to_csv(f"{reportout}/csv/rd.averages.full.csv",index=False)
print(f"Combined CSV: {reportout}/csv/rd.averages.full.csv")
# endregion

# region CLOSE-FOOTER
logging.info(f"************ REPORT GEN COMPLETED")
# endregion
