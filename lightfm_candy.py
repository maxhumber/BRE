from copy import deepcopy
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import csr_matrix
from matplotlib import pyplot as plt

# # TODO:
# builder for interactions
# euclidean_distances model using just sklearn
# spotlight example

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from lightfm import LightFM
from lightfm.evaluation import auc_score, precision_at_k

# Quick Data Prep

df = pd.read_csv('data/candy.csv')
df.sample(1)
# setup interactions

df=df.copy()
ratings='review'
users='user'
items='item'

ratings = np.array(df[ratings])
users = np.array(df[users])
items = np.array(df[items])

# heavy lifting encoders
user_encoder = LabelEncoder()
item_encoder = LabelEncoder()

# preparation for the csr matrix
u = user_encoder.fit_transform(users)
i = item_encoder.fit_transform(items)
lu = len(np.unique(u))
li = len(np.unique(i))

# the good stuff
interactions = csr_matrix((ratings, (u, i)), shape=(lu, li))

### train test split
from lightfm.cross_validation import random_train_test_split

train, test = random_train_test_split(interactions, test_percentage=0.2)

# model
model = LightFM(loss='warp')

count = 0
best = 0
auc = []
for e in range(100):
    if count > 5: # patience
        break
    model.fit_partial(train, epochs=1)
    auc_train = auc_score(model, train).mean()
    auc_test = auc_score(model, test).mean()
    print(f'Epoch: {e}, Train AUC={auc_train:.3f}, Test AUC={auc_test:.3f}')
    auc.append((auc_train, auc_test))
    if auc_test > best:
        best_model = deepcopy(model)
        best = auc_test
    else:
        count += 1
model = deepcopy(best_model)

auc = np.array(auc)
plt.plot(auc[:, 0], label='train')
plt.plot(auc[:, 1], label='test')
plt.legend()

precision_at_k(model, train, k=10).mean()
auc_score(model, test).mean()

user = 'aaron67'
df[df['user'] == user]

user_id = user_encoder.transform([user])[0]

preds = model.predict(user_id, list(range(li)))
preds = pd.DataFrame(zip(preds, item_encoder.classes_), columns=['pred', 'item'])
preds = preds.sort_values('pred', ascending=False)

tried = df[df['user'] == user]['item'].values
preds[~preds['item'].isin(tried)]['item'].values[:5]
