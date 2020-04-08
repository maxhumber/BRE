import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
from flask import Flask, request, render_template

app = Flask(__name__, template_folder="templates")

with open("model.pkl", "rb") as f:
    import cloudpickle
    model = cloudpickle.load(f)

@app.route("/")
def index():
    repos = model.cv.get_feature_names()
    random_candy = ", ".join(random.choices(repos, k=5))
    return render_template("index.html", random_candy=random_candy)

@app.route("/result", methods=["POST"])
def predict():
    candy = request.form["candy"]
    candy = ",".join([c.strip() for c in candy.split(", ")])
    suggestions = model.predict([candy])[0]
    random.shuffle(suggestions)
    return render_template("result.html", suggestions=suggestions[:5])

if __name__ == "__main__":
    app.run(debug=True, port=8000)
