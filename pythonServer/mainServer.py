import flask
from flask import request, make_response

app = flask.Flask(__name__)


@app.route('/product', methods=['GET', 'POST'])
def processProduct():
    if request.method == 'POST':
        data = request.get_json()
        productInfo = {
            "name": f"{data.get('productName')}",
            "units": f"{data['units']}",
            "price": f"{data['price']}",
            "numRatings": f"{data['numRatings']}",
            "numStars": f"{data['numStars']}",
            "description": f"{data['description']}",
            "asin": f"{data['asin']}"
        }
        response = make_response(productInfo, 200)  # wait for josh to do NLP bullshit
        return response
