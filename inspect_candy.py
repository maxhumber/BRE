import pandas as pd

df1 = pd.read_csv('data/candy-1.csv')
df2 = pd.read_csv('data/candy-2.csv')
df3 = pd.read_csv('data/candy-3.csv')

df = pd.concat([df1, df2, df3])
df = df.reset_index(drop=True)
df.to_csv('data/candy.csv', index=False)

df = pd.read_csv('data/candy.csv')

df.info()

len(df['user'].unique())

df['user'].value_counts()[df['user'].value_counts() >= 5]

df[df['user'] == 'jenniferh55']
