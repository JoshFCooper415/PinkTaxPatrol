import flask
from flask import request

app = flask.Flask(__name__)


@app.route('/product', methods=['GET,POST'])
def processProduct():
    if request.method == 'POST':
        data = request.get_json()
        productInfo = {
            "name": f"{data['productName']}",
            "units": data["units"],
            "price": data["price"],
            "numRatings": data["numRatings"],
            "numStars": data["numStars"],
            "description": f"{data['description']}",
            "asin": f"{data['asin']}"
        }
        response = make_response()
