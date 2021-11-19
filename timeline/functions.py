# region IMPORTS
import datetime
from datetime import timedelta
import os
from os.path import exists

import json
import pandas as pd
from pandas import json_normalize
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import logging

# endregion

def mastertable(d,rawpath):

    runtimes = os.listdir(rawpath)
    runtimes = sorted(runtimes, reverse=True)
    print(runtimes)
    logging.info(f"Crawl Runtimes: {runtimes}")

    level = ["All", "Legend", "Mythic"]

    # START THE CRAWLER
    dfx = pd.DataFrame(columns=['runtime', 'name', 'win', 'use', 'ban', 'wrank', 'urank', 'banrank', 'elo'])
    for lvl in level:
        
        for pt in runtimes[:d]:

            # constructoutput
            jsonfile = f'{rawpath}/{pt}/{lvl}.json'
            if os.path.exists(jsonfile):
                print("Requesting: " + jsonfile)
                logging.info("Requesting: " + jsonfile)

                ##### BUILD TABLES ####
                with open(jsonfile) as j:
                    data = json.load(j)

                    df = json_normalize(data, ['data', 'data'])

                    # convert from strings:
                    df['win'] = list(map(lambda x: x[:-1], df['win'].values))
                    df['use'] = list(map(lambda x: x[:-1], df['use'].values))
                    df['ban'] = list(map(lambda x: x[:-1], df['ban'].values))

                    df['win'] = [float(x) for x in df['win'].values]
                    df['use'] = [float(x) for x in df['use'].values]
                    df['ban'] = [float(x) for x in df['ban'].values]

                    # add ranking column
                    df = df.sort_values(by=['use'], ascending=False)
                    df['urank'] = range(1, len(df) + 1)
                    df = df.sort_values(by=['win'], ascending=False)
                    df['wrank'] = range(1, len(df) + 1)
                    df = df.sort_values(by=['ban'], ascending=False)
                    df['banrank'] = range(1, len(df) + 1)

                    df['runtime'] = f"{pt}"
                    df['elo'] = f"{lvl}"

                    dfx = pd.concat([dfx, df], axis=0)
                    dfx = dfx.sort_values('runtime', axis=0, ascending=True)
            else:
                print(f"Bad Request: Missing: {jsonfile}")
                logging.warning(f"Bad Request: Missing: {jsonfile}")

        # TEST OUT TO CSV
    
    print(f"Combined:{lvl}-\n{dfx}")
    return dfx
    

        
