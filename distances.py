from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd

# toying around

df = pd.read_csv('data/candy.csv')
df = df[df['user'].isin(df['user'].sample(10))]
df = df.pivot(index='item', columns='user', values='review').reset_index()
df.head(1)

df = df.melt(id_vars='item', var_name='user', value_name='review')
df = df.dropna().reset_index(drop=True)
df

# data shaping

df = pd.DataFrame([
    [0, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 0],
    [1, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 1],
    [0, 0, 0, 1, 1, 1]
])

euclidean_distances(df)

##


df = pd.read_csv("data/candy.csv")

df = df.groupby(["user"])["repo"].apply(lambda x: ",".join(x))
df = pd.DataFrame(df)

class NNRecommender:
    def __init__(
        self, n_neighbors=10, max_features=1000, tokenizer=lambda x: x.split(",")
    ):
        self.cv = CountVectorizer(tokenizer=tokenizer, max_features=max_features)
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)

    def fit(self, X):
        self.X = X
        X = self.cv.fit_transform(X)
        self.nn.fit(X)
        return self

    def predict(self, X):
        Xp = []
        for Xi in X:
            Xt = self.cv.transform([Xi])
            _, neighbors = self.nn.kneighbors(Xt)
            repos = []
            for n in neighbors[0]:
                r = self.X.iloc[int(n)].split(",")
                repos.extend(r)
            repos = list(set(repos))
            repos = [r for r in repos if r not in Xi.split(",")]
            Xp.append(repos)
        return Xp

n_neighbors = 10
max_features = 1000
model = NNRecommender(n_neighbors, max_features)
model.fit(df["repo"])

with open("model/model.pkl", "wb") as f:
    dill.dump(model, f)
