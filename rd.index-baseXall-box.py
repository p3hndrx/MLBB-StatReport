# region IMPORTS
import datetime
from datetime import timedelta
import os

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea, OffsetImage, AnnotationBbox

import logging

# endregion

# region ENVIRONMENT
logging.basicConfig(filename="/tmp/sync-reportgen.rd-type4.log", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")
logging.info(f"********************** STARTING REPORT GEN - BASE X ALL - BOX (RANKED DATA)")
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
reportout = "/var/www/html/reports/baseXall-box.rd"


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
                rslt_df = rslt_df.sort_values(by=[str(c)],ascending=False).head(10)
                rslt_df = rslt_df[['name', 'win','use','ban']]

                if c == "win":
                    clabel = "WinRate%"
                elif c == "ban":
                    clabel = "BAN"
                elif c == "use":
                    clabel = "Use%"

                #print(f"{rslt_df}")

                top = rslt_df['name'].tolist()
                print(f"{top}")
                dfc = dfx[dfx['name'].isin(top)]
                dfc = dfc.sort_values(by=[str(c)], ascending=False)

                print(f"{dfc}")
                #input("Press Enter to continue...")


                # BOX GRAPH PLOT
                fig, ax = plt.subplots(facecolor='darkslategrey')
                plt.style.use('dark_background')

                dfc.reset_index(inplace=True)
                df2 = pd.DataFrame({col: vals[str(c)] for col, vals in dfc.groupby(['name'])})
                meds = df2.median().sort_values()
                print(meds)
                ax = df2[meds.index].boxplot(ax=ax, return_type="axes", showmeans=True, fontsize=8, grid=False,
                                             positions=range(len(top)))
                # ax = dfc.boxplot(column=str(c), by=['name'], ax=ax, showmeans=True, fontsize=8, grid=False,positions=range(len(top)))

                ax.set(xlabel=None, title=None)
                plt.xticks(rotation=15)

                plt.title(
                    f'Top Heroes by {clabel} (As of {d})\nPeriod: {ptitle.capitalize()}, Elo: {lvl}',
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
                #print(f"{y}")

                i = 0
                # for i, (name, data) in enumerate(dfc.groupby('name')):
                for (name, data) in meds.iteritems():
                    xy = (i, y)
                    shero = name.replace("-", "").replace("'", "").replace(".", "").replace(" ", "").lower()
                    fn = f"{imgsrc}/{shero}.png"  # path to file
                    arr_img = plt.imread(fn, format='png')
                    imagebox = OffsetImage(arr_img, zoom=0.125)
                    imagebox.image.axes = ax

                    trans = ax.get_xaxis_transform()
                    ab = AnnotationBbox(imagebox, xy, xybox=(0, -15), xycoords=trans, boxcoords="offset points", pad=0,
                                        frameon=False)
                    ax.add_artist(ab)
                    i += 1

                i = 0
                # for i, (name, data) in enumerate(dfc.groupby('name')):
                for (name, data) in meds.iteritems():
                    df = rslt_df[rslt_df['name'] == name]
                    df = df.round(2)
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
                    i += 1

                # file output
                #plt.show()
                op = f"{reportout}/{ptitle}.{lvl}.{c}.png"
                plt.savefig(op, transparent=False, bbox_inches="tight")
                print(f"Combined Image: {op}")
                logging.info(f"Combined Image: {op}")

                plt.close('all')
            #input("Press Enter to continue...")


# endregion

# region CLOSE-FOOTER
logging.info(f"************ REPORT GEN COMPLETED")
# endregion
