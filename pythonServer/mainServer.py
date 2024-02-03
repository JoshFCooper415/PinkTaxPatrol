import flask
import numpy
from flask import request, make_response
import numpy as np
import joblib
import lightbeam
import sklearn

app = flask.Flask(__name__)


@app.route('/product', methods=['GET', 'POST'])
def processProduct():
    if request.method == 'POST':
        data = request.get_json()
        productInfo = {
            "name": f"{data['productName']}",
            "units": f"{data['units']}",
            "price": f"{data['price']}",
            "numRatings": f"{data['numRatings']}",
            "numStars": f"{data['numStars']}",
            "description": f"{data['description']}",
            "asin": f"{data['asin']}"
        }

        inferFromModel(productName=productInfo.get("name"))
        response = make_response(productInfo, 200)  # wait for josh to do NLP bullshit
        return response


def inferFromModel(productName: str):
    rf = joblib.load("../Data/lgbm_classifier_model.joblib")
    validWords = np.load("../Data/col_names.npy")
    words = np.char.split(productName, " ")

    mask = np.isin(words, validWords)
    words = words[mask]

    np.sort(words)

    wordFixer = np.vectorize(align_words)
    words = wordFixer(words, validWords)


print(np.load("../Data/col_names.npy", allow_pickle=True))


def align_words(words, valid_words):
    aligned_words = []
    for word in valid_words:
        if word in words:
            aligned_words.append(word)
        else:
            aligned_words.append(0)
    return aligned_words

# Example usage:
