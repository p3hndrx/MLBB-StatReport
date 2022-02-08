# region IMPORTS
import datetime
from datetime import timedelta
import os
from os.path import exists

import json
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
from matplotlib import dates as mdates

import logging
# endregion

# region ENVIRONMENT
logging.basicConfig(filename="/tmp/sync-summarygen.rd.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
logging.info(f"********************** STARTING SUMMARY GEN - RANKDATA")
# endregion

# region VARIABLES
x = datetime.datetime.now()
y = x - timedelta(days = 1)
today = x.strftime("%Y%m%d")
logging.info(f"Runtime: {today}")
yesterday = y.strftime("%Y%m%d")

rawpath = "/tmp/RankData.fake"
outpath = "/tmp/summary.rd"
avgoutpath = "/tmp/averages.rd"
imgsrc = "/Users/phunr/PycharmProjects/MLBB-StatReport/heroes"

runtimes = os.listdir(rawpath)
runtimes = sorted(runtimes, reverse=True)
print(runtimes)
logging.info(f"Crawl Runtimes: {runtimes}")


level = ["All","Legend","Mythic"]
period = ["day7","day30","day90"]

# endregion

# region CHECK PATHS
 # File Count
for folder in runtimes:
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
   

 # Generate Folders
if not os.path.exists(outpath):
    os.system(f"mkdir {outpath}")
else:
    print(f"{outpath} Exists.")
if not os.path.exists(avgoutpath):
    os.system(f"mkdir {avgoutpath}")
else:
    print(f"{avgoutpath} Exists.")

for lvl in level:
    outputcheck = f"{outpath}/{lvl}"
    if not os.path.exists(outputcheck):
        os.system(f"mkdir {outputcheck}")
        print(f"Making Folder: {outputcheck}")
        logging.info(f"Making Folder: {outputcheck}")
    else:
        print(f"Exists: {outputcheck}")
        logging.info(f"Exists: {outputcheck}")

    avgoutputcheck = f"{avgoutpath}/{lvl}"
    if not os.path.exists(avgoutputcheck):
        os.system(f"mkdir {avgoutputcheck}")
        print(f"Making Folder: {avgoutputcheck}")
        logging.info(f"Making Folder: {avgoutputcheck}")
    else:
        print(f"Exists: {avgoutputcheck}")
        logging.info(f"Exists: {avgoutputcheck}")

    for tp in period:
        tpavgoutputcheck = f"{outputcheck}/{tp}"
        if not os.path.exists(tpavgoutputcheck):
            os.system(f"mkdir {tpavgoutputcheck}")
            print(f"Making Folder: {tpavgoutputcheck}")
            logging.info(f"Making Folder: {tpavgoutputcheck}")
        else:
            print(f"Exists: {tpavgoutputcheck}")
            logging.info(f"Exists: {tpavgoutputcheck}")

        tpsumgoutputcheck = f"{avgoutputcheck}/{tp}"
        if not os.path.exists(tpsumgoutputcheck):
            os.system(f"mkdir {tpsumgoutputcheck}")
            print(f"Making Folder: {tpsumgoutputcheck}")
            logging.info(f"Making Folder: {tpsumgoutputcheck}")
        else:
            print(f"Exists: {tpsumgoutputcheck}")
            logging.info(f"Exists: {tpsumgoutputcheck}")

# endregion

# region GEN FUNCTION
for tp in period:
    if tp == "day7":
        d = 7
        dt = "Week"
    elif tp == "day30":
        d = 30
        dt = "Month"
    elif tp == "day90":
        d = 90
        dt = "Season"

    print(f"Running: {dt}:{tp}")

    for lvl in level:
        from functions import mastertable
        dfx = mastertable(d,rawpath)

        dfx = dfx[dfx['elo'].str.contains(lvl)]
        #heroes = dfx.groupby('name')
        heroes = dfx['name'].unique()
        for hero in heroes:
            plt.style.use('dark_background')
            #TEST OUT TO CSV
            #outfilename = hero + '.csv'
            #print(outfilename)

            #OUTPUT LINECHART
            df2 = dfx[dfx['name'] == hero]
            df2 = df2[['runtime','win','use','ban']]
            print(f"{hero}\n{df2}")


            shero = hero.replace("-", "").replace("'", "").replace(".", "").replace(" ", "").lower()
            op = f"{outpath}/{lvl}/{tp}/{shero}.png"
            outlier = 0

            #fig, ax = plt.subplots(facecolor='darkslategrey')
            fig, axs = plt.subplots(nrows=3, figsize=(7, 5), facecolor='darkslategrey', sharex=True)
            for ax, column, color, (min_normal, max_normal) in zip(axs,
                                                                   ['win', 'use', 'ban'],
                                                                   ['springgreen', 'gold', 'tomato'],
                                                                   [(40, 60), (0.01, 5), (0.05, 80)]):

                df2.plot(x='runtime', xlabel="Date", y=column, ylabel=column,kind='line', marker='o', linewidth=2, alpha=.7, color=color, legend=False, ax=ax)
                #df_abnormal = df2[(df2[column] < min_normal) | (df2[column] > max_normal)]
                #df_abnormal.plot(x='runtime', xlabel="Date", y=column, ylabel=column,kind='scatter', marker='D',color='white', legend=False, zorder=3, ax=ax)
                ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
                #if not df_abnormal.empty:
                #    outlier+=1

            plt.style.use('dark_background')
            plt.xticks(rotation=15)

            #df2.plot(x='runtime',xlabel="Date", kind='line', marker='o',linewidth=2,alpha=.7,subplots=True,color=['khaki', 'lightcyan','thistle'])
            plt.suptitle(f'Historical Data for {hero}\nElo: {lvl}', fontsize=12,fontname = 'monospace')

            shero = hero.replace("-", "").replace("'", "").replace(".", "").replace(" ", "").lower()
            print(f"Searching {shero} from {hero}")
            logging.debug(f"Searching {shero} from {hero}")

            # Generate Coordinates
            # search
            xy = (0, 0)

            fn = get_sample_data(f"{imgsrc}/{shero}.png", asfileobj=False)
            arr_img = plt.imread(fn, format='png')

            imgax = fig.add_axes([0.05, 0.9, 0.1, 0.1], zorder=1)
            imgax.imshow(arr_img)
            imgax.axis('off')

            #if outlier >= 1:
            #    print(f"We have an outlier.")
            #    plt.figtext(0, 0.01, "*NOTE: A statistically improbable anomaly was detected in the data you have requested.",
            #                fontsize=9,fontname='monospace', color='black',bbox={"facecolor":"yellow", "alpha":0.5, "pad":5})

            #file output
            plt.savefig(op, transparent=False,bbox_inches="tight")


            print(f"Output Plot: {op}")
            logging.info(f"Output Plot: {op}")
            #plt.show()
            plt.close('all')

            #OUTPUT AVERAGES
            op = f"{avgoutpath}/{lvl}/{tp}/{shero}.png"


            #fig, ax = plt.subplots(facecolor='darkslategrey')
            fig, (ax1, ax2, ax3) = plt.subplots(1,3,facecolor='darkslategrey', sharex=False, sharey=False)
            ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            ax3.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            df2.boxplot('win',ax=ax1,showmeans=True, fontsize=10, grid=False)
            df2.boxplot('use',ax=ax2,showmeans=True, fontsize=10, grid=False)
            df2.boxplot('ban',ax=ax3,showmeans=True, fontsize=10, grid=False)
            plt.style.use('dark_background')
            plt.suptitle(f'Summary Data for {hero}\nElo: {lvl}', fontsize=12,fontname = 'monospace')


            shero = hero.replace("-", "").replace("'", "").replace(".", "").replace(" ", "").lower()
            print(f"Searching {shero} from {hero}")
            logging.debug(f"Searching {shero} from {hero}")

            # Generate Coordinates
            # search
            xy = (0, 0)

            fn = get_sample_data(f"{imgsrc}/{shero}.png", asfileobj=False)
            arr_img = plt.imread(fn, format='png')

            imgax = fig.add_axes([0.05, 0.9, 0.1, 0.1], zorder=1)
            imgax.imshow(arr_img)
            imgax.axis('off')


            #for axis in ax:
            #    print(type(axis))
            plt.tight_layout()
            #file output
            plt.savefig(op, transparent=False,bbox_inches="tight")


            print(f"Output Plot: {op}")
            logging.info(f"Output Plot: {op}")
            #plt.show()
            plt.close('all')
# endregion

# region CLOSE-FOOTER
logging.info(f"************ SUMMARY GEN COMPLETED")
# endregion
