import requests
import pandas as pd

# Function to fetch product data
def fetch_product_data(product, gender, rapidapi_key):
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    querystring = {"query": f"Cheap {product} for {gender}"}
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        return response.json()['data']['products']
    else:
        print(f"Failed to fetch data for {product} for {gender}: {response.status_code}")
        return []

# Function to parse and return the product data in a structured format
def parse_product_data(products, category, gender):
    structured_data = []
    for product in products:
        structured_data.append({
            'ASIN': product['asin'],
            'Product Name': product['product_title'],
            'Category': category,
            'Keyword': gender,
            'Unit Count': product.get('unit_count', 'N/A'),
            'Number of Reviews': product['product_num_ratings'],
            'Average Review Score': product['product_star_rating'],
            'Manufacturer' : '',
            'Price': product['product_price'],
            
        })
    return structured_data

# Main function to fetch and save data
def main(rapidapi_key):
    products = ['razors', 'shampoo', 'deodorant', 'lotion', 'soap', 'conditioner', 'condoms']
    genders = ['women', 'men']
    all_products_info = []

    for product in products:
        for gender in genders:
            fetched_products = fetch_product_data(product, gender, rapidapi_key)
            if fetched_products:
                structured_data = parse_product_data(fetched_products, product, gender)
                all_products_info.extend(structured_data)

    # Convert all the product info into a pandas DataFrame
    df = pd.DataFrame(all_products_info)

    # Save the DataFrame to a CSV file
    csv_file_path = 'amazon_products_via_rainforest_api6.csv'
    df.to_csv(csv_file_path, index=False)
    print(f"Data saved to {csv_file_path}")

# Replace YOUR_RAPIDAPI_KEY with your actual RapidAPI key
rapidapi_key = 'aa773b1d34msh85dc2f34e692807p1dcac6jsna2bcd6271c95'
main(rapidapi_key)
