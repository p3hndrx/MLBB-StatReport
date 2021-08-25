# region IMPORTS
import datetime
from datetime import timedelta
import os
from os.path import exists

import json
import pandas as pd
import matplotlib.pyplot as plt

import logging

# endregion

# region ENVIRONMENT
logging.basicConfig(filename="/tmp/sync-summarygen.log", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")
logging.info(f"********************** STARTING SUMMARY GEN V2")
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
runtimes = os.listdir(rawpath)
runtimes = sorted(runtimes, reverse=True)
print(runtimes)
logging.info(f"Crawl Runtimes: {runtimes}")

bfruntimes = os.listdir(csvpath)
bfruntimes = sorted(bfruntimes, reverse=True)
print(bfruntimes)
logging.info(f"Crawl BackFill Runtimes: {bfruntimes}")

# DATASETS
lang = ["en"]
region = ["all", "NA", "EU", "SA", "SE"]
dtrange = ["Week"]
mode = ["All-Modes", "Classic", "Rank", "Brawl"]
level = ["All-Levels", "Normal", "High", "Very-High"]

# endregion

# region CHECK PATHS
# File Count
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

    print(f"{folder}:{totalFiles}")
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

    print(f"{bfolder}:{totalBFiles}")
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
        print(f"Exists: {outputcheck}")
        logging.info(f"Exists: {outputcheck}")
    for m in mode:
        moutputcheck = f"{outputcheck}/{m}"
        if not os.path.exists(moutputcheck):
            os.system(f"mkdir {moutputcheck}")
            print(f"Making Folder: {moutputcheck}")
            logging.info(f"Making Folder: {moutputcheck}")
        else:
            print(f"Exists: {moutputcheck}")
            logging.info(f"Exists: {moutputcheck}")
        for lvl in level:
            loutputcheck = f"{moutputcheck}/{lvl}"
            if not os.path.exists(loutputcheck):
                os.system(f"mkdir {loutputcheck}")
                print(f"Making Folder: {loutputcheck}")
                logging.info(f"Making Folder: {loutputcheck}")
            else:
                print(f"Exists: {loutputcheck}")
                logging.info(f"Exists: {loutputcheck}")
# Generate Folders (Averages)
for r in region:
    avgoutputcheck = f"{avgoutpath}/{r}"
    if not os.path.exists(avgoutputcheck):
        os.system(f"mkdir {avgoutputcheck}")
        print(f"Making Folder: {avgoutputcheck}")
        logging.info(f"Making Folder: {avgoutputcheck}")
    else:
        print(f"Exists: {avgoutputcheck}")
        logging.info(f"Exists: {avgoutputcheck}")
    for m in mode:
        avgmoutputcheck = f"{avgoutputcheck}/{m}"
        if not os.path.exists(avgmoutputcheck):
            os.system(f"mkdir {avgmoutputcheck}")
            print(f"Making Folder: {avgmoutputcheck}")
            logging.info(f"Making Folder: {avgmoutputcheck}")
        else:
            print(f"Exists: {avgmoutputcheck}")
            logging.info(f"Exists: {avgmoutputcheck}")
        for lvl in level:
            avgloutputcheck = f"{avgmoutputcheck}/{lvl}"
            if not os.path.exists(avgloutputcheck):
                os.system(f"mkdir {avgloutputcheck}")
                print(f"Making Folder: {avgloutputcheck}")
                logging.info(f"Making Folder: {avgloutputcheck}")
            else:
                print(f"Exists: {avgloutputcheck}")
                logging.info(f"Exists: {avgloutputcheck}")
# endregion

# region TIMELINE + AVERAGES
print("Compiling Lookup")
logging.info("Compiling Lookup")

# Create master table
runtimes = runtimes + bfruntimes
runtimes = sorted(runtimes, reverse=False)

# START THE CRAWLER
i = 0
t = 0

for l in lang:
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
                            print("Requesting: " + csvfile)
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
                            print(f"Bad Request: Missing {csvfile}")
                            logging.warning(f"Bad Request: Missing: {csvfile}")

                        # constructoutput
                        jsonfile = f'{rawpath}/{pt}/en/{r}/{dt}.{lvl}.{m}.json'
                        if os.path.exists(jsonfile):
                            print("Requesting: " + jsonfile)
                            logging.info("Requesting: " + jsonfile)

                            ##### BUILD TABLES ####
                            with open(jsonfile) as j:
                                data = json.load(j)
                                rows = [v for k, v in data["data"].items()]

                                df = pd.DataFrame(rows, columns=['name', 'win', 'use', 'kda'])
                                df['win'] = df['win'].str.rstrip('%').astype('float')
                                df['use'] = df['use'].str.rstrip('%').astype('float')
                                # df['win'] = pd.to_numeric(df['win'])
                                df['runtime'] = f"{pt}"
                                df['runtime'] = df['runtime'].astype('datetime64[ns]')
                                df['region'] = f"{r}"
                                df['period'] = f"{dt}"
                                df['elo'] = f"{lvl}"
                                df['mode'] = f"{m}"
                                dfx = pd.concat([dfx, df], axis=0)
                        else:
                            print(f"Bad Request: Missing: {jsonfile}")
                            logging.warning(f"Bad Request: Missing: {jsonfile}")

                    # TEST OUT TO CSV
                    # dfx.to_csv(f"{outpath}/{r}/{m}/{lvl}.csv",index=False)
                    # print(f"Combined:{lvl}-{m}-{r}\n{dfx}")
                    # logging.info(f"Combined:{lvl}-{m}-{r}\n{dfx}")

                    # heroes = dfx.groupby('name')
                    heroes = dfx['name'].unique()
                    for hero in heroes:
                        plt.style.use('dark_background')
                        # TEST OUT TO CSV
                        # outfilename = hero + '.csv'
                        # print(outfilename)

                        # OUTPUT LINECHART
                        df2 = dfx[dfx['name'] == hero]
                        df2 = df2[['runtime', 'win', 'use', 'kda']]
                        print(f"{hero}\n{df2}")

                        shero = hero.replace("-", "").replace("'", "").replace(".", "").replace(" ", "").lower()
                        op = f"{outpath}/{r}/{m}/{lvl}/{shero}.png"

                        # fig, ax = plt.subplots(facecolor='darkslategrey')
                        fig, axs = plt.subplots(nrows=3, figsize=(7, 5), facecolor='darkslategrey', sharex=True)
                        for ax, column, color, (min_normal, max_normal) in zip(axs,
                                                                               ['win', 'use', 'kda'],
                                                                               ['khaki', 'lightcyan', 'thistle'],
                                                                               [(10, 90), (0.05, 10), (0.05, 10)]):
                            df2.plot(x='runtime', xlabel="Date", y=column, ylabel=column, kind='line', marker='o',
                                     linewidth=2, alpha=.7, color=color, legend=False, ax=ax)
                            df_abnormal = df2[(df2[column] < min_normal) | (df2[column] > max_normal)]
                            df_abnormal.plot(x='runtime', xlabel="Date", y=column, ylabel=column, kind='scatter',
                                             marker='D', color='red', legend=False, zorder=3, ax=ax)
                        plt.style.use('dark_background')
                        plt.xticks(rotation=15)
                        # df2.plot(x='runtime',xlabel="Date", kind='line', marker='o',linewidth=2,alpha=.7,subplots=True,color=['khaki', 'lightcyan','thistle'])
                        plt.suptitle(f'Historical Data for {hero}\nRegion: {r}, Elo: {lvl}, Mode:{m}', fontsize=12,
                                     fontname='monospace')

                        if (df2['kda'] > 20).any() or (df2['kda'] < .05).any() or (df2['win'] == 100).any() or (
                                df2['use'] == 0).any():
                            print(f"We have an outlier.")
                            plt.figtext(0, 0.01,
                                        "*NOTE: A statistically improbable anomaly was detected in the data you have requested.",
                                        fontsize=9, fontname='monospace', color='black',
                                        bbox={"facecolor": "yellow", "alpha": 0.5, "pad": 5})

                        # file output
                        plt.savefig(op, transparent=False, bbox_inches="tight")

                        print(f"Output Plot: {op}")
                        logging.info(f"Output Plot: {op}")
                        # plt.show()
                        plt.close('all')

                        # OUTPUT AVERAGES
                        op = f"{avgoutpath}/{r}/{m}/{lvl}/{shero}.png"

                        # fig, ax = plt.subplots(facecolor='darkslategrey')
                        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, facecolor='darkslategrey', sharex=False, sharey=False)
                        df2.boxplot('win', ax=ax1, showmeans=True, fontsize=10, grid=False)
                        df2.boxplot('use', ax=ax2, showmeans=True, fontsize=10, grid=False)
                        df2.boxplot('kda', ax=ax3, showmeans=True, fontsize=10, grid=False)
                        plt.style.use('dark_background')
                        plt.suptitle(f'Summary Data for {hero}\nRegion: {r}, Elo: {lvl}, Mode:{m}', fontsize=12,
                                     fontname='monospace')
                        # for axis in ax:
                        #    print(type(axis))
                        plt.tight_layout()
                        # file output
                        plt.savefig(op, transparent=False, bbox_inches="tight")

                        print(f"Output Plot: {op}")
                        logging.info(f"Output Plot: {op}")
                        # plt.show()
                        plt.close('all')
# endregion

# region CLOSE-FOOTER
logging.info(f"************ SUMMARY GEN COMPLETED")
# endregion
