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
import heroicons

# endregion

# region ENVIRONMENT
logging.basicConfig(filename="/tmp/sync-reportgen-type5.log", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")
logging.info(f"********************** STARTING REPORT GEN - RECENT SUMMARY")
print("Starting Report Gen...")
# endregion

# region VARIABLES
x = datetime.datetime.now()
y = x - timedelta(days=1)
today = x.strftime("%Y%m%d")
logging.info(f"Runtime: {today}")
yesterday = y.strftime("%Y%m%d")

# PATHS
rawpath = "/tmp/RankData.fake"
reportout = "/tmp/report"


# GENERATE FOLDER LISTS
print("Checking Folder Paths...")

runtimes = os.listdir(rawpath)
runtimes = sorted(runtimes, reverse=True)
#print(runtimes)
logging.info(f"Crawl Runtimes: {runtimes}")

# DATASETS
crit = ['win','use','ban']
#dtrange = ["Week"]
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
print("Compiling Lookup...")
logging.info("Compiling Lookup")

# Create master table
runtimes = sorted(runtimes, reverse=True)

# START THE CRAWLER
from functions import statstable
dfx = statstable(7, rawpath)

print(dfx)

#Find Professions
print(f"Checking Professions:")
dfx['role'] = '-'

for p in prof:
    print(f"Matching {p}:")
    rslt = getattr(roles, p)

    dfx.loc[dfx.name.isin(rslt), 'role'] = p
dfx = dfx.round(2)

# TEST OUT TO CSV
print(f"Source Table... \n{dfx}")
dfx.to_csv(f"{reportout}/rd.master.csv",index=False)
print(f"Combined CSV: {reportout}/master.csv")
#input("Press Enter to continue...")

# endregion

# region CLOSE-FOOTER
logging.info(f"************ REPORT GEN COMPLETED")
# endregion
