import requests
import pandas as pd
def search_amazon_via_rainforest(api_key, category, search_term, amazon_domain='amazon.com', sort_by='most_recent'):
    base_url = 'https://api.rainforestapi.com/request'
    params = {
        'api_key': api_key,
        'type': 'search',
        'amazon_domain': amazon_domain,
        'search_term': f"{search_term} {category}",
        'sort_by': sort_by
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {search_term} {category}: {response.status_code}")
        return None

# Replace 'YOUR_API_KEY' with your actual Rainforest API key
API_KEY = '396B94246D9346309EFE0DE4A156A748'  # IMPORTANT: Replace with your actual API key

# Define your categories and search terms here
categories = ['razors', 'shampoo', 'deodorant', 'lotion', 'soap', 'conditioner', 'condoms']
keywords = ['women', 'men']

results = []

# Iterate over categories and keywords, making API requests
for category in categories:
    for keyword in keywords:
        data = search_amazon_via_rainforest(API_KEY, category, keyword)
        if data and 'search_results' in data:
            for item in data['search_results']:
                if 'asin' in item:
                    # Initialize price and unit_count to None or a default value
                    price = None
                    unit_count = None
                    
                    # Example of extracting price, adjust based on actual API response structure
                    if 'price' in item and 'value' in item['price']:
                        price = item['price']['value']
                    
                    # Example of extracting amount per purchase or unit count, adjust as necessary
                    if 'unit_count' in item:  # Assuming 'unit_count' is directly available
                        unit_count = item['unit_count']
                    results.append({
                        'ASIN': item['asin'],
                        'Product Name': item.get('title'),
                        'Category': category,
                        'Keyword': keyword,
                        'Number of Reviews': item.get('ratings_total'),
                        'Average Review Score': item.get('rating'),
                        'Manufacturer': item.get('brand'),
                        'Price': price,
                        'Unit Count': unit_count
                    })
                    

# Convert the results into a DataFrame
df = pd.DataFrame(results)

# Save the DataFrame to a CSV file
df.to_csv('amazon_products_via_rainforest_api4.csv', index=False)