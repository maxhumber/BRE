import pandas as pd

df = pd.read_csv('data/stars.csv')

df.head(1)
df['repo'].value_counts()[df['repo'].value_counts() >= 5]
