# region IMPORTS
import datetime
from datetime import timedelta
import os

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
from matplotlib import dates as mdates

import logging

# endregion

# region ENVIRONMENT
logging.basicConfig(filename="/tmp/sync-reportgen.rd-type3.log", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")
logging.info(f"********************** STARTING REPORT GEN - BASE X ALL (RANKED DATA)")
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
imgsrc = "/root/MLBB-StatReport/heroes"
reportout = "/var/www/html/reports/baseXall.rd"


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
periods = [7,30,90]

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
runtimes = sorted(runtimes, reverse=True)

# START THE CRAWLER
i = 0
t = 0

for lvl in level:
    from functions import statstable

    for period in periods:
        if period == 7:
            ptitle = "week"
        elif period == 30:
            ptitle = "month"
        elif period ==90:
            ptitle = "season"

        dfx = statstable(period, rawpath)

        dfx = dfx[dfx['elo'].str.contains(lvl)]

        fig, ax = plt.subplots(facecolor='darkslategrey')
        plt.style.use('dark_background')

        #print(len(dfx))
        if len(dfx) == 0:
            logging.info(f"No events for: {lvl}; {period}")
        else:
            latest = dfx['runtime'].iloc[-1]

            print(latest)

            for c in crit:

                d = latest.strftime("%m/%d/%Y")

                # Get top heroes by each criteria
                print(f"Last Date: {latest}; Top: {c}")
                logging.info(f"Last Date: {latest}; Top: {c}")
                rslt_df = dfx[dfx['runtime'] == latest]
                print(f"Latest Run: {rslt_df}")
                rslt_df = rslt_df.sort_values(by=[str(c)], ascending=False).head(5)
                rslt_df = rslt_df[['name', 'win', 'use', 'ban']]

                if c == "win":
                    clabel = "WinRate%"
                elif c == "ban":
                    clabel = "BAN"
                elif c == "use":
                    clabel = "Use%"

                print(f"{rslt_df}")

                top = rslt_df['name'].tolist()
                # print(f"{top}")
                dfc = dfx[dfx['name'].isin(top)]
                dfc.sort_values(by=[str(c)], ascending=False)
                print(f"{dfc}")
                # input("Press Enter to continue...")

                # HISTORICAL GRAPH PLOT
                fig, ax = plt.subplots(facecolor='darkslategrey')
                plt.style.use('dark_background')

                dfc.pivot(index='runtime', columns='name', values=c).plot(figsize=(10, 5), marker='o', linewidth=2, ax=ax)
                plt.xticks(rotation=15)

                plt.suptitle(
                    f'Historical Top 5 by {clabel} (As of {d})\nPeriod: {ptitle.capitalize()}, Elo: {lvl}',
                    fontsize=12,
                    fontname='monospace')
                plt.legend(loc=2)
                ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
                ax.xaxis.set_minor_formatter(mdates.DateFormatter(''))
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

                # LABEL
                print("Generating Labels...")
                logging.info(f"Generating Labels...")
                for hero in top:
                    shero = hero.replace("-", "").replace("'", "").replace(".", "").replace(" ", "").lower()
                    print(f"Searching {shero} from {hero}")
                    logging.debug(f"Searching {shero} from {hero}")

                    # Generate Coordinates
                    # search
                    dfh = rslt_df[rslt_df['name'] == hero]
                    val = dfh[str(c)].values[0]
                    val = round(val,2)
                    xy = (d, val)

                    fn = get_sample_data(f"{imgsrc}/{shero}.png", asfileobj=False)
                    arr_img = plt.imread(fn, format='png')
                    imagebox = OffsetImage(arr_img, zoom=0.125)
                    imagebox.image.axes = ax

                    print(fn)
                    ab = AnnotationBbox(imagebox, xy,
                                        xybox=(15., 0),
                                        xycoords='data',
                                        boxcoords="offset points",
                                        pad=0,
                                        frameon=False
                                        )
                    logging.info(f"Coord: {xy}")
                    print(f"Coord: {xy}")
                    ax.add_artist(ab)

                    # Fix the display limits to see everything
                    # ax.set_xlim(0, 1)
                    # ax.set_ylim(0, 1)

                # file output
                # plt.show()
                op = f"{reportout}/{ptitle}.{lvl}.{c}.png"
                plt.savefig(op, transparent=False, bbox_inches="tight")
                print(f"Combined Image: {op}")
                logging.info(f"Combined Image: {op}")

                plt.close('all')
            # input("Press Enter to continue...")

# endregion

# region CLOSE-FOOTER
logging.info(f"************ REPORT GEN COMPLETED")
# endregion
