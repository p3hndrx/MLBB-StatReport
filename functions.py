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

# region VARIABLES

APIpath = "/var/www/html/MLBB-API/v1/"
herofile = "hero-meta-final.json"
prof = ["assassin","marksman","mage","tank","support","fighter"]
lanes = ["gold","exp","mid","jungle","roam"]
# IMPORT MOJI MAP
with open(APIpath+herofile) as j:
    data = json.load(j)

    df = json_normalize(data, ['data'])
    df = df[df.hero_name != 'None']

    # fix punctuation
    df.replace('Chang-e', 'Chang\'e')
    df.replace('X-Borg', 'X.Borg')

    ### get hero moji (replaces mojimap.py)
    moji = df.set_index('uid')['discordmoji'].to_dict()


# endregion

# region MAIN
def statstable(d, rawpath):
    runtimes = os.listdir(rawpath)
    runtimes = sorted(runtimes, reverse=True)
    print(runtimes)
    logging.info(f"Crawl Runtimes: {runtimes}")

    level = ["All", "Legend", "Mythic"]
    prof = ["assassin", "marksman", "mage", "tank", "support", "fighter"]

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

                    df['win'] = df['win'].round(2)
                    df['use'] = df['use'].round(2)
                    df['ban'] = df['ban'].round(2)

                    # add ranking column
                    df = df.sort_values(by=['use'], ascending=False)
                    df['urank'] = range(1, len(df) + 1)
                    df = df.sort_values(by=['win'], ascending=False)
                    df['wrank'] = range(1, len(df) + 1)
                    df = df.sort_values(by=['ban'], ascending=False)
                    df['banrank'] = range(1, len(df) + 1)

                    df['runtime'] = f"{pt}"
                    df['runtime'] = df['runtime'].astype('datetime64[ns]')
                    df['elo'] = f"{lvl}"

                    dfx = pd.concat([dfx, df], axis=0)
                    dfx = dfx.sort_values('runtime', axis=0, ascending=True)
                    dfx = dfx[dfx['win'] != 0]
            else:
                print(f"Bad Request: Missing: {jsonfile}")
                logging.warning(f"Bad Request: Missing: {jsonfile}")

        # TEST OUT TO CSV
    for p in prof:
        #print(f"Matching {p}:")
        rslt = getattr(roles, p)

        dfx.loc[dfx.name.isin(rslt), 'role'] = p


    #print(f"Combined:{lvl}-\n{dfx}")
    return dfx

# endregion

# region API Functions


def heroesgen():
    jsonfile = APIpath + herofile

    if os.path.exists(jsonfile):
        print("Requesting: " + jsonfile)
        logging.info("Requesting: " + jsonfile)

        ##### BUILD LOOKUP TABLES ####
        with open(jsonfile) as j:
            data = json.load(j)

            df = json_normalize(data, ['data'])
            df = df[df.hero_name != 'None']

            #CONCISE FILTER
            dfh = df[["hero_name","mlid","uid","hero_icon","discordmoji","portrait","laning","class"]]
            #print(dfh)


            ### generate role groups (replaces roles.py)
            class roles:
                for role in prof:
                    role = str(role)
                    role = role.capitalize()

                    dfr = df.set_index('class').filter(like=role, axis=0)
                    dfr = dfr[["hero_name"]]

                    # fix punctuation
                    dfr = dfr.replace(['Chang-e'], 'Chang\'e')
                    dfr = dfr.replace(['X-Borg'], 'X.Borg')
                    dfr = dfr.replace(['Yi Sun-Shin'], 'Yi Sun-shin')
                    #print(dfr)
                    #print(f"{role}:{dfr}")

                    if role == "Fighter":
                        fighter = dfr['hero_name'].tolist()
                    if role == "Tank":
                        tank = dfr['hero_name'].tolist()
                    if role == "Support":
                        support = dfr['hero_name'].tolist()
                    if role == "Assassin":
                        assassin = dfr['hero_name'].tolist()
                    if role == "Marksman":
                        marksman = dfr['hero_name'].tolist()
                    if role == "Mage":
                        mage = dfr['hero_name'].tolist()

            return roles

roles = heroesgen()
# endregion

#hlist, portrait, moji, laning, roles = heroesgen()
#print(hlist)
