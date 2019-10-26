import pandas as pd
from faker import Faker # pip install Faker

df = pd.read_csv('data/candy.csv')
usernames_real = list(df['user'].value_counts()[df['user'].value_counts() >= 5].index)
df = df[df['user'].isin(usernames_real)]

fake = Faker()

usernames_fake = []
while len(usernames_fake) < len(usernames_real):
    name = fake.user_name()
    if name not in usernames_fake:
        usernames_fake.append(name)

assert len(set(usernames_fake)) == len(usernames_fake)
assert len(usernames_fake) == len(usernames_real)

username_replacements = {r: f for r, f in zip(usernames_real, usernames_fake)}

dff = df.copy()
dff['user'] = dff['user'].replace(username_replacements)
df = dff.copy()

df['product'] = df['product'].str.replace('/reviews/', '')
products = pd.DataFrame(df['product'].value_counts())
products = products.reset_index()
products['fixed'] = products['index'].str.replace('-', ' ')
products = products.sort_values('fixed')
products['fixed'] = products['fixed'].apply(lambda x: ' '.join(i.capitalize() for i in x.split(' ')))
products.to_csv('data/manual_candy.csv', index=False)

# small manual edits

products = pd.read_csv('data/manual_candy.csv')

# join

df = pd.merge(df, products, on='product', how='left')
df = df[['candy', 'user', 'stars']]
df.columns = ['item', 'user', 'review']
df.to_csv('data/candy_edit.csv', index=False)

#
