import requests
import json

productInfo = {
    "productName": "Aussie Instant Freeze Hair Spray Triple Pack for Curly Hair, Straight Hair, and Wavy Hair, 10 fl oz (Pack of 3)",
    "productCostWhole": "14.",
    "productCostFraction": "96",
    "listProducts": "Product Dimensions \u200f : \u200e 2.16 x 6.44 x 9.64 inches; 2.07 Pounds+++Item model number \u200f : \u200e 4354622585+++UPC \u200f : \u200e 381519080166 381519191213+++Manufacturer \u200f : \u200e Procter & Gamble - Pampers+++ASIN \u200f : \u200e B07NFQTB5G+++Country of Origin \u200f : \u200e USA",
    "productReviewCount": "8,999 ratings",
    "productReviewRating": "4.4 out of 5 stars"
}
r = requests.post("http://127.0.0.1:5000/product", json=productInfo)
print(r.status_code)
print(r.json())
