import pandas as pd

df = pd.read_csv('data/candy.csv')
df2 = pd.read_csv('data/candy-4.csv')

df = pd.concat([df, df2]).reset_index(drop=True)
df = df.drop_duplicates()
df.to_csv('data/candy_1000.csv', index=False)


users = df['user'].value_counts()[df['user'].value_counts() >= 5].index
df = df[df['user'].isin(users)]

pd.DataFrame(df['product'].value_counts())



#
