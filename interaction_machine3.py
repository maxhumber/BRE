import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import csr_matrix
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from lightfm import LightFM

# Quick Data Prep

df = pd.read_csv('data/candy.csv')
users = df['user'].value_counts()[df['user'].value_counts() >= 5].index
df = df[df['user'].isin(users)]
df['product'] = df['product'].str.replace('/reviews/', '')

# setup interactions

df=df.copy()
ratings='stars'
users='user'
items='product'

_ratings = np.array(df[ratings])
_users = np.array(df[users])
_items = np.array(df[items])

# heavy lifting encoders
user_encoder = LabelEncoder()
item_encoder = LabelEncoder()

# preparation for the csr matrix
u = user_encoder.fit_transform(_users)
i = item_encoder.fit_transform(_items)
lu = len(np.unique(u))
li = len(np.unique(i))

# the good stuff
interactions = csr_matrix((_ratings, (u, i)), shape=(lu, li))


### train test split
from lightfm.cross_validation import random_train_test_split

train, test = random_train_test_split(interactions, test_percentage=0.2)

# model
from lightfm.evaluation import auc_score

model = LightFM(loss='warp')

auc = []
for e in range(100):
    model.fit_partial(train, epochs=1)
    auc_train = auc_score(model, train).mean()
    auc_test = auc_score(model, test).mean()
    auc.append((auc_train, auc_test))
auc = np.array(auc)

from matplotlib import pyplot as plt

plt.plot(auc[:, 0], label='train')
plt.plot(auc[:, 1], label='test')
plt.legend()

user_encoder.classes_[0]

preds = model.predict(0, list(range(li)))
preds = pd.DataFrame(zip(preds, item_encoder.classes_), columns=['pred', 'product'])
preds = preds.sort_values('pred', ascending=False)

tried = df[df['user'] == '07julia12']['product'].values
preds[~preds['product'].isin(tried)]['product'].values[:5]


# # TODO:
# Automatic filtering of predictions
# overfitting early stopper
# builder for
# euclidean_distances model using just sklearn
# spotlight example
