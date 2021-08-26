import pandas as pd
import numpy as np

names = ['PersonA', 'PersonB', 'PersonC', 'PersonD']
dates = pd.date_range(start = '2021-05-28', end = '2021-08-23', freq = 'D')

df = pd.DataFrame({'runtime': np.repeat(dates, len(names))})
df['name'] = len(dates)*names
df['A'] = 40 + 20*np.random.random(len(df))
df['B'] = .1 * np.random.random(len(df))
df['C'] = 1 +.5 * np.random.random(len(df))

print(f"{df}")