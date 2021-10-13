# region IMPORTS
import datetime
from datetime import timedelta
import os
from os.path import exists

import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
from matplotlib import dates as mdates

import logging
import roles
import heroicons

# endregion

# region ENVIRONMENT
logging.basicConfig(filename="/tmp/sync-reportgen-type4.log", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")
logging.info(f"********************** STARTING REPORT GEN - BASE X MODE-BOX")
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
reportout = "/Users/phunr/var/www/html/output/report/baseXmode-box"


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

for r in region:
    outputcheck = f"{reportout}/{r}"
    if not os.path.exists(outputcheck):
        os.system(f"mkdir {outputcheck}")
        print(f"Making Folder: {outputcheck}")
        logging.info(f"Making Folder: {outputcheck}")
    else:
        #print(f"Exists: {outputcheck}")
        logging.info(f"Exists: {outputcheck}")
    for lvl in level:
        loutputcheck = f"{outputcheck}/{lvl}"
        if not os.path.exists(loutputcheck):
            os.system(f"mkdir {loutputcheck}")
            print(f"Making Folder: {loutputcheck}")
            logging.info(f"Making Folder: {loutputcheck}")
        else:
            #print(f"Exists: {loutputcheck}")
            logging.info(f"Exists: {loutputcheck}")

# endregion

# region TIMELINE GEN
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
            dfx = pd.DataFrame(
                columns=['runtime', 'name', 'win', 'use', 'kda', 'region', 'period', 'elo', 'mode'])
            for m in mode:
                for lvl in level:
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
                    # dfx.drop(dfx[dfx['win'] == 100].index, inplace=True)
                    # dfx.drop(dfx[dfx['use'] <= .001].index, inplace=True)
                    # dfx.drop(dfx[dfx['kda'] >= 20].index, inplace=True)
                    #dfx = dfx[dfx.use >= .001]
                    #dfx = dfx[dfx.win != 100]
                    dfx = dfx[dfx.kda <= 20]

            # TEST OUT TO CSV
            print(f"Source Table... \n{dfx}")
            dfx.to_csv(f"{reportout}/{r}.csv",index=False)
            print(f"Combined CSV: {reportout}/{r}.csv")
            logging.info(f"Combined CSV: {reportout}/{r}.csv")
            #input("Press Enter to continue...")


            fig, ax = plt.subplots(facecolor='darkslategrey')
            plt.style.use('dark_background')

            for md in mode:
                print(f"Cycling Modes...{r}-{md}:")
                logging.info(f"Cycling Modes...{r}-{md}:")

                dfm = dfx[dfx['mode']==md]
                print(f"{dfm}")
                #input("Press Enter to continue...")

                for l in level:
                    print(f"Cycling Level...{r}-{md}-{l}:")
                    logging.info(f"Cycling Modes...{r}-{md}-{l}:")
                    dfl = dfm[dfm['elo'] == l]
                    print(f"{dfl}")
                    #input("Press Enter to continue...")

                    for c in crit:
                        # FILTER top 5:
                        latest = dfm['runtime'].iloc[-1]
                        d = latest.strftime("%m/%d/%Y")

                        #Get top heroes by each criteria
                        print(f"Last Date: {latest}; Top: {c}")
                        logging.info(f"Last Date: {latest}; Top: {c}")
                        rslt_df = dfl[dfl['runtime'] == latest]
                        rslt_df = rslt_df.sort_values(by=[str(c)],ascending=False).head(10)
                        rslt_df = rslt_df[['name','win','use','kda']]

                        if c == "win":
                            clabel = "WinRate%"
                        elif c == "kda":
                            clabel = "KDA"
                        elif c == "use":
                            clabel = "Use%"

                        print(f"{rslt_df}")

                        top = rslt_df['name'].tolist()
                        print(f"{top}")
                        dfc = dfl[dfl['name'].isin(top)]
                        dfc.sort_values(by=[str(c)], ascending=1)

                        # BOX GRAPH PLOT
                        fig, ax = plt.subplots(facecolor='darkslategrey')
                        plt.style.use('dark_background')

                        ax = dfc.boxplot(column=str(c), by=['name'], ax=ax, showmeans=True, fontsize=8, grid=False,
                                         positions=range(len(top)))
                        ax.set(xlabel=None, title=None)
                        plt.xticks(rotation=15)

                        md = md.capitalize()
                        #r = r.capitalize()
                        plt.title(
                            f'Top Heroes in {md} by {clabel} (As of {d})\nRegion: {r}, Elo: {l}',
                            fontsize=12,
                            fontname='monospace')
                        plt.suptitle('')

                        # LABEL
                        print("Generating Labels...")
                        logging.info(f"Generating Labels...")

                        # move the xtick labels
                        ax.set_xticks(range(len(top)))
                        ax.tick_params(axis='x', which='major', pad=20)

                        # use the ytick values to locate the image

                        y = ax.get_xticks()[0]
                        # print(f"{y}")

                        for i, (name, data) in enumerate(dfc.groupby('name')):
                            xy = (i, y)

                            shero = name.replace("-", "").replace("'", "").replace(".", "").replace(" ", "").lower()
                            fn = f"{imgsrc}/{shero}.png"  # path to file
                            arr_img = plt.imread(fn, format='png')
                            imagebox = OffsetImage(arr_img, zoom=0.125)
                            imagebox.image.axes = ax

                            trans = ax.get_xaxis_transform()
                            ab = AnnotationBbox(imagebox, xy, xybox=(0, -15), xycoords=trans, boxcoords="offset points",
                                                pad=0, frameon=False)
                            ax.add_artist(ab)

                        for i, (name, data) in enumerate(dfc.groupby('name')):
                            df = rslt_df[rslt_df['name'] == name]
                            y2 = df.iloc[0][str(c)]
                            xy2 = (i, y2)
                            xy = (i, y)
                            ax.plot(xy2[0], xy2[1], "oy")
                            offsetbox = TextArea(f"{y2}", textprops=dict(color="white", fontsize="small"))

                            trans = ax.get_xaxis_transform()
                            ab = AnnotationBbox(offsetbox, xy,
                                                xybox=(0, 10),
                                                xycoords=trans,
                                                boxcoords="offset points",
                                                pad=0, frameon=False)
                            # arrowprops=dict(arrowstyle="->")
                            ax.add_artist(ab)
                            print(f"{name}:{xy}")
                            # input("Press Enter to continue...")

                        # file output
                        # plt.show()
                        op = f"{reportout}/{r}/{l}/{md}.{c}.png"
                        plt.savefig(op, transparent=False, bbox_inches="tight")
                        print(f"Combined Image: {op}")
                        logging.info(f"Combined Image: {op}")

                        plt.close('all')


# endregion

# region CLOSE-FOOTER
logging.info(f"************ REPORT GEN COMPLETED")
# endregion
