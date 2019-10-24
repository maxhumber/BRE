import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import csr_matrix

from sklearn.metrics.pairwise import euclidean_distances

df = pd.DataFrame([
    [0, 1, 0, 1, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0]
])

euclidean_distances(df)

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from lightfm import LightFM

# Quick Data Prep

df = pd.read_csv('data/candy.csv')
users = df['user'].value_counts()[df['user'].value_counts() >= 5].index
df = df[df['user'].isin(users)]

# The Magic

class InteractionMachine:

    def __init__(self, df, ratings, users, items):
        self._ratings = np.array(df[ratings])
        self._users = np.array(df[users])
        self._items = np.array(df[items])
        # heavy lifting encoders
        self.user_encoder = LabelEncoder()
        self.item_encoder = LabelEncoder()
        # preparation for the csr matrix
        u = self.user_encoder.fit_transform(self._users)
        i = self.item_encoder.fit_transform(self._items)
        uu = len(np.unique(u))
        ui = len(np.unique(i))
        # the good stuff
        self.interactions = csr_matrix((self._ratings, (u, i)), shape=(uu, ui))

    def get_users(self, encoded=False):
        users = np.unique(self._users)
        if encoded:
            users = self.user_encoder.transform(users)
        return users

    def get_items(self, encoded=False):
        items = np.unique(self._items)
        if encoded:
            items = self.item_encoder.transform(items)
        return items

df.head(1)

im = InteractionMachine(df, 'stars', 'user', 'product')
im.interactions

im.get_items(encoded=True)

im.get_users(encoded=False)

pd.DataFrame(
    im.interactions.todense(),
    index = im.get_users(),
    columns = im.get_items()
)

model = LightFM()

model.fit(im.interactions, epochs=20)

person = 'kitkatkittikat'
user_id = im.user_encoder.transform([person])[0]
preds = model.predict(user_id, im.get_items(encoded=True))

pred_df = pd.DataFrame({
    'product': im.get_items(),
    'rating': preds
}).sort_values('rating', ascending=False)
pred_df

reco = pred_df['product'].values.tolist()

tried = df[df['user'] == person]['product'].tolist()

[candy for candy in reco if candy not in tried][:5]


person = 'kitkatkittikat'
df[df['user'] == person]
