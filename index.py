# region IMPORTS
import datetime
from datetime import timedelta
import os
from os.path import exists

import json
import pandas as pd
import matplotlib.pyplot as plt

import logging

import roles

# endregion

# region ENVIRONMENT
logging.basicConfig(filename="/tmp/sync-reportgen.log", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")
logging.info(f"********************** STARTING REPORT GEN V1")
print("Starting Report Gen...")
# endregion

# region VARIABLES
x = datetime.datetime.now()
y = x - timedelta(days=1)
today = x.strftime("%Y%m%d")
logging.info(f"Runtime: {today}")
yesterday = y.strftime("%Y%m%d")

# PATHS
rawpath = "/Users/phunr/var/www/html/TierData/json"
csvpath = "/Users/phunr/var/www/html/TierData/backfill"
outpath = "/Users/phunr/var/www/html/output/sum"
avgoutpath = "/Users/phunr/var/www/html/output/avg"

# report vars
reportout = "/Users/phunr/var/www/html/output/report"
src = "/Users/phunr/var/www/html/src"

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
for r in region:
    outputcheck = f"{outpath}/{r}"
    if not os.path.exists(outputcheck):
        os.system(f"mkdir {outputcheck}")
        print(f"Making Folder: {outputcheck}")
        logging.info(f"Making Folder: {outputcheck}")
    else:
        #print(f"Exists: {outputcheck}")
        logging.info(f"Exists: {outputcheck}")
    for m in mode:
        moutputcheck = f"{outputcheck}/{m}"
        if not os.path.exists(moutputcheck):
            os.system(f"mkdir {moutputcheck}")
            print(f"Making Folder: {moutputcheck}")
            logging.info(f"Making Folder: {moutputcheck}")
        else:
            #print(f"Exists: {moutputcheck}")
            logging.info(f"Exists: {moutputcheck}")
        for lvl in level:
            loutputcheck = f"{moutputcheck}/{lvl}"
            if not os.path.exists(loutputcheck):
                os.system(f"mkdir {loutputcheck}")
                print(f"Making Folder: {loutputcheck}")
                logging.info(f"Making Folder: {loutputcheck}")
            else:
                #print(f"Exists: {loutputcheck}")
                logging.info(f"Exists: {loutputcheck}")
# Generate Folders (Averages)
for r in region:
    avgoutputcheck = f"{avgoutpath}/{r}"
    if not os.path.exists(avgoutputcheck):
        os.system(f"mkdir {avgoutputcheck}")
        print(f"Making Folder: {avgoutputcheck}")
        logging.info(f"Making Folder: {avgoutputcheck}")
    else:
        #print(f"Exists: {avgoutputcheck}")
        logging.info(f"Exists: {avgoutputcheck}")
    for m in mode:
        avgmoutputcheck = f"{avgoutputcheck}/{m}"
        if not os.path.exists(avgmoutputcheck):
            os.system(f"mkdir {avgmoutputcheck}")
            print(f"Making Folder: {avgmoutputcheck}")
            logging.info(f"Making Folder: {avgmoutputcheck}")
        else:
            #print(f"Exists: {avgmoutputcheck}")
            logging.info(f"Exists: {avgmoutputcheck}")
        for lvl in level:
            avgloutputcheck = f"{avgmoutputcheck}/{lvl}"
            if not os.path.exists(avgloutputcheck):
                os.system(f"mkdir {avgloutputcheck}")
                print(f"Making Folder: {avgloutputcheck}")
                logging.info(f"Making Folder: {avgloutputcheck}")
            else:
                #print(f"Exists: {avgloutputcheck}")
                logging.info(f"Exists: {avgloutputcheck}")
# endregion

# region TIMELINE + AVERAGES
print("Compiling Lookup...")
logging.info("Compiling Lookup")

# Create master table
runtimes = runtimes + bfruntimes
runtimes = sorted(runtimes, reverse=False)

# START THE CRAWLER
i = 0
t = 0

for l in lang:
    #dfx = pd.DataFrame(
         #columns=['runtime', 'name', 'win', 'use', 'kda', 'region', 'period', 'elo', 'mode'])
    for r in region:
        for dt in dtrange:
            for m in mode:
                for lvl in level:
                    dfx = pd.DataFrame(
                        columns=['runtime', 'name', 'win', 'use', 'kda', 'region', 'period', 'elo', 'mode'])
                    for pt in runtimes[:90]:

                        # constructbackfill
                        csvfile = f'{csvpath}/{pt}/en/{r}/{dt}.{lvl}.{m}.csv'
                        if os.path.exists(csvfile):
                            #print("Requesting: " + csvfile)
                            logging.info("Requesting: " + csvfile)

                            dfc = pd.read_csv(csvfile, sep=r'\s*,\s*', skipinitialspace=True, header=0,
                                              encoding='ascii', engine='python')
                            # print(dfc)
                            dfc = dfc[['name', 'win', 'use', 'kda']]
                            dfc['win'] = dfc['win'].str.rstrip('%').astype('float')
                            dfc['use'] = dfc['use'].str.rstrip('%').astype('float')
                            # df['win'] = pd.to_numeric(df['win'])
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
                    logging.info(f"Combined CSV: {reportout}/{r}.{m}.{lvl}.csv")
                    dfx.drop(dfx[dfx['win'] == 100].index, inplace=True)
                    dfx.drop(dfx[dfx['use'] <= .001].index, inplace=True)
                    dfx.drop(dfx[dfx['kda'] >= 20].index, inplace=True)

                    # TEST OUT TO CSV
                    print(f"Source Table... \n{dfx}")
                    dfx.to_csv(f"{reportout}/{r}.{m}.{lvl}.csv",index=False)
                    print(f"Combined CSV: {reportout}/{r}.{m}.{lvl}.csv")
                    logging.info(f"Combined CSV: {reportout}/{r}.{m}.{lvl}.csv")
                    #input("Press Enter to continue...")
    #TEST MAIN OUT
    #print(f"{dfx}")
    #dfx.to_csv(f"{reportout}/master.csv", index=False)
    #print(f"Combined CSV: {reportout}/master.csv")
    #logging.info(f"Combined CSV: {reportout}/master.csv")
    #input("Press Enter to continue...")


                    for p in prof:
                        print(f"Cycling Roles...{r}.{m}.{lvl}.{p}:")
                        report = "\n"
                        rslt = getattr(roles, p)
                        dfp = dfx[dfx['name'].isin(rslt)]
                        print(f"{dfp}")

                        #FILTER top 5:
                        crit = ['win','use','kda']
                        latest = dfp['runtime'].iloc[-1]

                        for c in crit:
                            print(f"Last Date: {latest}; Top: {c}")
                            rslt_df = dfp[dfp['runtime'] == latest]
                            rslt_df = rslt_df.sort_values(by=[str(c)]).head(5)
                            #print(f"{rslt_df}")
                            #input("Press Enter to continue...")

                            #print(f"{rslt_df['name']}")
                            top = rslt_df['name'].tolist()
                            print(f"{top}")
                            input("Press Enter to continue...")
                            dfc = dfp[dfp['name'].isin(top)]
                            dfc.sort(by=[str(c)], ascending=[1, 0])

                            #Graph:
                            print(f"Charting Changes...{r}.{m}.{lvl}.{p}: by {c}")
                            plt.style.use('dark_background')
                            op = f"{reportout}/{r}.{m}.{lvl}.{p}.{c}.png"
                            n = len(pd.unique(dfc['name']))

                            fig, ax = plt.subplots(nrows=n, sharex=True)
                            #dfp.pivot(index='runtime', columns='name', values='win').plot(subplots=True, layout=(n, 1), figsize=(6, 9), marker='o',linewidth=2)
                            for i, name in enumerate(dfc['name'].unique(), 0):
                                df_filtered = dfc[dfc['name'] == name]
                                ax[i].plot(df_filtered['runtime'], df_filtered[str(c)], marker='o', linewidth=2)
                                ax[i].set_ylabel(name)

                            plt.style.use('dark_background')
                            plt.xticks(rotation=15)
                            plt.suptitle(f'Historical Data for {p}\nRegion: {r}, Elo: {lvl}, Mode:{m}', fontsize=12,
                                     fontname='monospace')
                            # file output
                            plt.savefig(op, transparent=False, bbox_inches="tight")

                            print(f"Combined Image: {op}")
                            logging.info(f"Combined Image: {op}")
                            #plt.show()
                            plt.close('all')
                            input("Press Enter to continue...")


# endregion

# region CLOSE-FOOTER
logging.info(f"************ SUMMARY GEN COMPLETED")
# endregion
