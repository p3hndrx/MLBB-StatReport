# region IMPORTS
import datetime
from datetime import timedelta
import os

import json
import pandas as pd
import numpy as np

import logging
import roles


# endregion

# region ENVIRONMENT
logging.basicConfig(filename="/tmp/sync-reportgen-type4.log", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")
logging.info(f"********************** STARTING REPORT GEN - REGIONX")
print("Starting Report Gen...")
# endregion

# region VARIABLES
x = datetime.datetime.now()
y = x - timedelta(days=1)
today = x.strftime("%Y%m%d")
logging.info(f"Runtime: {today}")
yesterday = y.strftime("%Y%m%d")

# PATHS
#rawpath = "/var/www/html/TierData/json"
#csvpath = "/var/www/html/TierData/backfill"
#imgsrc = "/root/MLBB-StatReport/heroes"
#reportout = "/var/www/html/reports/baseXrole"

# DEVPATHS
rawpath = "/Users/phunr/var/www/html/TierData/json"
csvpath = "/Users/phunr/var/www/html/TierData/backfill"
imgsrc = "/Users/phunr/PycharmProjects/MLBB-StatReport/heroes"
reportout = "/Users/phunr/var/www/html/output/report/master"


# GENERATE FOLDER LISTS
print("Checking Folder Paths...")

runtimes = os.listdir(rawpath)
runtimes = sorted(runtimes, reverse=True)
#print(runtimes)
logging.info(f"Crawl Runtimes: {runtimes}")

bfruntimes = os.listdir(csvpath)
bfruntimes = sorted(bfruntimes, reverse=True)
#print(bfruntimes)
logging.info(f"Crawl BackFill Runtimes: {bfruntimes}")

# DATASETS
crit = ['win','use','kda']
lang = ["en"]
region = ["all", "NA", "EU", "SA", "SE"]
dtrange = ["Week"]
mode = ["All-Modes", "Classic", "Rank", "Brawl"]
level = ["All-Levels", "Normal", "High", "Very-High"]
prof = ["assassin","marksman","mage","tank","support","fighter"]

# endregion

# region CHECK PATHS
# File Count
print("Counting Source Files...")
for folder in runtimes:
    # count = os.system(f"find {rawpath}{folder} -type f | wc -l")
    totalFiles = 0
    totalDir = 0

    for base, dirs, files in os.walk(f"{rawpath}/{folder}"):
        #    print('Searching in : ',base)
        logging.info(f"Searching: {base}")
        for directories in dirs:
            totalDir += 1
        for Files in files:
            totalFiles += 1

    #print(f"{folder}:{totalFiles}")
    logging.info(f"Folder: {folder}")
    logging.info(f"Files: {totalFiles}")
    # print('Total Number of directories',totalDir)
    # print('Total:',(totalDir + totalFiles))

for bfolder in bfruntimes:
    totalBFiles = 0
    totalBDir = 0
    for base, bdirs, bfiles in os.walk(f"{csvpath}/{bfolder}"):
        logging.info(f"Searching: {base}")
        for bdirectories in bdirs:
            totalBDir += 1
        for bFiles in bfiles:
            totalBFiles += 1

    #print(f"{bfolder}:{totalBFiles}")
    logging.info(f"Folder: {bfolder}")
    logging.info(f"Files: {totalBFiles}")
    # print('Total Number of directories',totalBDir)
    # print('Total:',(totalBDir + totalBFiles))

# Generate Folders
if not os.path.exists(reportout):
    os.system(f"mkdir {reportout}")
    print(f"Making Folder: {reportout}")
    logging.info(f"Making Folder: {reportout}")

# endregion

# region TIMELINE GEN
print("Compiling Lookup...")
logging.info("Compiling Lookup")

# Create master table
runtimes = runtimes + bfruntimes
runtimes = sorted(runtimes, reverse=True)

# START THE CRAWLER
i = 0
t = 0

for l in lang:
    dfx = pd.DataFrame(
         columns=['runtime', 'name', 'win', 'use', 'kda', 'region', 'period', 'elo', 'mode','role'])
    for r in region:
        #dfx = pd.DataFrame(columns=['runtime', 'name', 'win', 'use', 'kda', 'region', 'period', 'elo', 'mode'])
        for dt in dtrange:
            for m in mode:
                for lvl in level:
                    for pt in runtimes[:2]:

                        # constructbackfill
                        csvfile = f'{csvpath}/{pt}/en/{r}/{dt}.{lvl}.{m}.csv'
                        if os.path.exists(csvfile):
                            print("Requesting: " + csvfile)
                            logging.info("Requesting: " + csvfile)

                            dfc = pd.read_csv(csvfile, sep=r'\s*,\s*', skipinitialspace=True, header=0,
                                              encoding='ascii', engine='python')
                            # print(dfc)
                            dfc = dfc[['name', 'win', 'use', 'kda']]
                            dfc['win'] = dfc['win'].str.rstrip('%').astype('float')
                            dfc['use'] = dfc['use'].str.rstrip('%').astype('float')
                            dfc['runtime'] = f"{pt}"
                            dfc['runtime'] = dfc['runtime'].astype('datetime64[ns]')
                            dfc['region'] = f"{r}"
                            dfc['period'] = f"{dt}"
                            dfc['elo'] = f"{lvl}"
                            dfc['mode'] = f"{m}"
                            dfx = pd.concat([dfx, dfc], axis=0)
                        else:
                            #print(f"Bad Request: Missing {csvfile}")
                            logging.warning(f"Bad Request: Missing: {csvfile}")

                        # constructoutput
                        jsonfile = f'{rawpath}/{pt}/en/{r}/{dt}.{lvl}.{m}.json'
                        if os.path.exists(jsonfile):
                            #print("Requesting: " + jsonfile)
                            logging.info("Requesting: " + jsonfile)

                            ##### BUILD TABLES ####
                            with open(jsonfile) as j:
                                data = json.load(j)
                                rows = [v for k, v in data["data"].items()]

                                df = pd.DataFrame(rows, columns=['name', 'win', 'use', 'kda'])
                                df['win'] = df['win'].str.rstrip('%').astype('float')
                                df['use'] = df['use'].str.rstrip('%').astype('float')
                                df['runtime'] = f"{pt}"
                                df['runtime'] = df['runtime'].astype('datetime64[ns]')
                                df['region'] = f"{r}"
                                df['period'] = f"{dt}"
                                df['elo'] = f"{lvl}"
                                df['mode'] = f"{m}"
                                dfx = pd.concat([dfx, df], axis=0)
                        else:
                            #print(f"Bad Request: Missing: {jsonfile}")
                            logging.warning(f"Bad Request: Missing: {jsonfile}")

    #Remove Outliers
    print(f"Removing Outliers...")
    logging.info(f"Combined CSV: {reportout}/master.csv")
    #dfx.drop(dfx[dfx['win'] == 100].index, inplace=True)
    #dfx.drop(dfx[dfx['use'] <= .001].index, inplace=True)
    #dfx.drop(dfx[dfx['kda'] >= 10].index, inplace=True)
    mediankda = dfx.loc[dfx['kda'] < 8, 'kda'].median()
    medianuse = dfx.loc[dfx['use'] < 10, 'use'].median()
    dfx['use'] = dfx['use'].mask(dfx['use'] > 10, medianuse)
    dfx['kda'] = dfx['kda'].mask(dfx['kda'] > 8, mediankda)

    #Find Professions
    print(f"Checking Professions:")
    for p in prof:
        print(f"Matching {p}:")
        rslt = getattr(roles, p)

        dfx.role = np.where(dfx['name'].isin(rslt), p, dfx.role)






    # TEST OUT TO CSV
    print(f"Source Table... \n{dfx}")
    dfx.to_csv(f"{reportout}/master.csv",index=False)
    print(f"Combined CSV: {reportout}/master.csv")
    logging.info(f"Combined CSV: {reportout}/{r}.csv")
    input("Press Enter to continue...")



# endregion

# region CLOSE-FOOTER
logging.info(f"************ REPORT GEN COMPLETED")
# endregion
