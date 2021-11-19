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
period = ["day1","day7","day30","day90","day365"]
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

# START THE CRAWLER

for tp in period:
    if tp == "day1":
        d = 1
        dt = "Day"
    elif tp == "day7":
        d = 7
        dt = "Week"
    elif tp == "day30":
        d = 30
        dt = "Month"
    elif tp == "day90":
        d = 90
        dt = "Season"
    elif tp == "day365":
        d = 365
        dt = "Year"

    print(f"RUnning: {dt}:{tp}")
    from functions import statstable
    dfx = statstable(d, rawpath)

    print(dfx)

    # TEST OUT TO CSV
    print(f"Source Table... \n{dfx}")
    dfx.to_csv(f"{reportout}/rd.{dt}.master.csv",index=False)
    print(f"Combined CSV: {reportout}/rd.{dt}.master.csv")
    #input("Press Enter to continue...")

# endregion

# region CLOSE-FOOTER
logging.info(f"************ REPORT GEN COMPLETED")
# endregion
