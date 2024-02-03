import requests
import json

productInfo = {
    "name": "Condoms",
    "units": "15",
    "price": "30",
    "numRatings": "37000",
    "numStars": "2.5",
    "description": "condoms to contain spunk",
    "asin": "389021809"
}
r = requests.post("http://127.0.0.1:5000/product", json=productInfo)
print(r.status_code)
print(r.json())
