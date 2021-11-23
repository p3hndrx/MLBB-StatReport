import pandas as pd
import numpy as np

names = ['PersonA', 'PersonB', 'PersonC', 'PersonD','PersonE','PersonF']
team = ['Team1','Team2']
dates = pd.date_range(start = '2020-05-28', end = '2021-11-22')

df = pd.DataFrame({'runtime': np.repeat(dates, len(names)*len(team))})
df['name'] = len(dates)*len(team)*names
df['team'] = len(dates)*len(names)*team
df['A'] = 40 + 20*np.random.random(len(df))
df['B'] = .1 * np.random.random(len(df))
df['C'] = 1 +.5 * np.random.random(len(df))


print(df)

df = df.groupby(['name','team'], as_index=True).apply(lambda gdf: gdf.assign(A_at=lambda gdf: gdf['A'].mean()))

print(df)