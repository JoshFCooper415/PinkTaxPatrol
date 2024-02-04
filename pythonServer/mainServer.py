import json

import flask
import numpy
from flask import request, make_response, jsonify
import numpy as np
import joblib
import lightbeam
import sklearn
import re
import csv
import pandas as pd
from pandas import DataFrame as df
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import joblib  # for saving and loading sklearn models
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)


@app.route('/product', methods=['GET', 'POST'])
def processProduct():
    if request.method == 'POST':
        data = request.get_json()
        #print(data)
        # todo: add ability to parse the actual recieved JSON
        productInfo = {
            "name": f"{data['productName']}",
            "priceCostWhole": f"{data['productCostWhole']}",
            "priceFraction": f"{data['productCostFraction']}",
            "listProducts": f"{data['listProducts']}",
            "productReviewCount": f"{data['productReviewCount']}",
            "productReviewRating": f"{data['productReviewRating']}",
        }
        data = sanatizeInfoDump(productInfo)
        data = getImportantDetails(data)
        print("DATA: ", data)

        results = inferFromModel(productName=productInfo.get("name"), productInfo=productInfo)
        response = make_response(results, 200)  #TODO: wait for josh to do NLP bullshit
        return response


def inferFromModel(productName: str, productInfo: dict):
    rf = joblib.load("../Data/lgbm_classifier_model.joblib")
    validWords = list(np.load("../Data/col_names.npy", allow_pickle=True))
    words = productName.lower().split(" ")
    words = np.array([word for word in words if word in validWords])  
    np.sort(words)
    words = np.unique(words)
    words = align_words(words, validWords)

    # Write the list of words to a CSV file
    with open("foo.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        for word in validWords:
            writer.writerow([word])

    wordFixer = np.vectorize(align_words)
    words = wordFixer(words, validWords)


    ASIN = productInfo['ASIN']
    ASINResult = reccomendedASINS(ASIN)

    RowResults = [query_DB(asin) for asin in ASINResult]
    deltaPrice = [float(productInfo['priceCostWhole'] + productInfo['priceFraction']) - row["Price"] for row in RowResults]
    productName = [row["Product Name"] for row in RowResults]
    links = [f"https://www.amazon.com/dp/{asinR}" for asinR in ASINResult]


    df = pd.DataFrame(words, columns=validWords)
    df['true_price'] = float(productInfo['priceCostWhole'] + productInfo['priceFraction'])

    rf.predict_proba(df)
    #TODO: JOSH FIX THIS PLEAAAAAAAAAAAAAAAASSSSSSSSSSSE
    return ASINResult,deltaPrice, productName, links

def query_DB(asin: str):
    df = pd.read_csv('../data/amazon_products_via_rainforest_api.csv')
    df2 = pd.read_csv('../data/amazon_products_via_rainforest_api2.csv')
    df3 = pd.read_csv('../data/amazon_products_via_rainforest_api3.csv')
    df4 = pd.read_csv('../data/amazon_products_via_rainforest_api4.csv')
    df5 = pd.read_csv('../data/amazon_products_via_rainforest_api5.csv')
    df6 = pd.read_csv('../data/amazon_products_via_rainforest_api6.csv')
    df7 = pd.read_csv('../data/amazon_products_via_rainforest_api7.csv')
    df5['Price'] = df5['Price'].str.replace('$', '').astype(float)
    df6['Price'] = df6['Price'].str.replace('$', '').astype(float)
    df7['Price'] = df7['Price'].str.replace('$', '').astype(float)

    # Display the first few rows of the dataframe
    df = pd.concat([df, df2, df3, df4, df5, df6, df7], axis=0)

    result = df[df["ASIN"] == asin]
    return result

def align_words(words, valid_words):
    aligned_words = []
    for word in valid_words:
        if word in words:
            aligned_words.append(word)
        else:
            aligned_words.append(0)
    return aligned_words


# Example usage:
def sanatizeInfoDump(infoDump: dict):
    print("")
    infoDump['listProducts'] = re.sub("[ ]{2,}", repl=" ", string=infoDump['listProducts'])
    infoDump['listProducts'] = re.sub(".u200.", repl="", string=infoDump['listProducts'])
    infoDump['listProducts'] = re.sub(r"\u200f : \u200e", repl=":", string=infoDump['listProducts'])

    # infoDump = re.sub("\\n", repl="", string=infoDump)

    return infoDump


def getImportantDetails(productJSON):
    listProducts = productJSON["listProducts"]
    manufacturterIndex = listProducts.find("Manufacturer")
    if manufacturterIndex != -1:
        listProducts[manufacturterIndex]

    # Split the input string by the delimiter "‏ : ‎"
    segments = listProducts.split("+++")

    endDict = {}
    #print(segments)
    # Iterate over the segments and extract data
    for segment in segments:
        # Clean up the segment
        segment = segment.strip()

        Datatype, information= segment.split(":")

        # print(product_dimensions, item_model_number, date_first_available, manufacturer, asin, country_of_origin)
        
        endDict.update({Datatype: information})

    del productJSON['listProducts']
    productJSON = {**productJSON, **endDict}
    return productJSON


#
#data = sanatizeInfoDump(""" {
#    "productName": "Trojan Bareskin Thin Premium Lubricated Condoms - 24 Count",
#    "productCostWhole": "15.",
#    "productCostFraction": "97",
#    "listProducts": "Is Discontinued By Manufacturer \u200f : \u200e No+++Product Dimensions \u200f : \u200e 1.81 x 5.13 x 5.19 inches; 2.4 Ounces+++Item model number \u200f : \u200e DL-409+++Department \u200f : \u200e mens, womens, uni sex adult,+++Date First Available \u200f : \u200e December 12, 2011+++Manufacturer \u200f : \u200e Church & Dwight - Personal Care+++ASIN \u200f : \u200e B008UYN4QA+++Country of Origin \u200f : \u200e Japan",
#    "productReviewCount": "15,144 ratings",
#    "productReviewRating": "4.6 out of 5 stars"
#}
#
# """)
# """

#data = getImportantDetails(data)


def preprocess_data(df, vectorizer=None, fit_vectorizer=True):
    """
    Applies all transformations to the dataframe `df`.

    Args:
    - df: pandas DataFrame, input data to transform.
    - vectorizer: CountVectorizer instance, if None a new one will be created and fit.
    - fit_vectorizer: bool, whether to fit the CountVectorizer or not (useful at inference).

    Returns:
    - df: transformed pandas DataFrame.
    - vectorizer: fitted CountVectorizer instance.
    """

    # Fit and transform the product names
    if vectorizer is None:
        vectorizer = CountVectorizer(binary=True)

    if fit_vectorizer:
        X = vectorizer.fit_transform(df['Product Name']).toarray()
    else:
        X = vectorizer.transform(df['Product Name']).toarray()

    # Create a DataFrame with the one-hot encoded features
    df_one_hot = pd.DataFrame(X, columns=vectorizer.get_feature_names_out(), index=df.index)
    # df = df.drop(['Product Name'])
    # Concatenate the original DataFrame with the new one-hot encoded DataFrame
    df = pd.concat([df, df_one_hot], axis=1)
    df.fillna(0, inplace=True)
    df['Unit Count'] = df['Unit Count'].replace(0, 1)  # Replace 0 units with 1 to avoid division by zero
    df['true_price'] = df['Price'] / df['Unit Count']
    df['Keyword'] = df['Keyword'].replace(
        {'men': 0, 'women': 1, 'missing': -1})  # Assuming 'missing' as -1 or another category

    # One-hot encode 'Category'
    one_hot_encoded = pd.get_dummies(df['Category'], prefix='Category')
    df = df.join(one_hot_encoded)

    # Replace spaces with underscores in column names and sort columns
    df.columns = [col.replace(' ', '') for col in df.columns]
    df = df.sort_index(axis=1)

    df = pd.read_csv('../data/amazon_products_via_rainforest_api.csv')
    df2 = pd.read_csv('../data/amazon_products_via_rainforest_api2.csv')
    df3 = pd.read_csv('../data/amazon_products_via_rainforest_api3.csv')
    df4 = pd.read_csv('../data/amazon_products_via_rainforest_api4.csv')
    df5 = pd.read_csv('../data/amazon_products_via_rainforest_api5.csv')
    df6 = pd.read_csv('../data/amazon_products_via_rainforest_api6.csv')
    df7 = pd.read_csv('../data/amazon_products_via_rainforest_api7.csv')
    df5['Price'] = df5['Price'].str.replace('$', '').astype(float)
    df6['Price'] = df6['Price'].str.replace('$', '').astype(float)
    df7['Price'] = df7['Price'].str.replace('$', '').astype(float)

    # Display the first few rows of the dataframe
    df = pd.concat([df, df2, df3, df4, df5, df6, df7], axis=0)

    # Example usage during training
    df, vectorizer = preprocess_data(df)
    df = df.drop(['Product_Name', 'ASIN', 'Category'], axis=1)
    print(df.columns.to_list())
    # Save the vectorizer for later use during inference
    joblib.dump(vectorizer, 'vectorizer.joblib')
    return df, vectorizer

def generateReccomendationDatabase():
    df = pd.read_csv('amazon_products_via_rainforest_api.csv')
    df2 = pd.read_csv('amazon_products_via_rainforest_api2.csv')
    df3 = pd.read_csv('amazon_products_via_rainforest_api3.csv')
    df4 = pd.read_csv('amazon_products_via_rainforest_api4.csv')
    df5 = pd.read_csv('amazon_products_via_rainforest_api5.csv')
    df6 = pd.read_csv('amazon_products_via_rainforest_api6.csv')
    df7 = pd.read_csv('amazon_products_via_rainforest_api7.csv')
    df5['Price'] = df5['Price'].str.replace('$', '').astype(float)
    df6['Price'] = df6['Price'].str.replace('$', '').astype(float)
    df7['Price'] = df7['Price'].str.replace('$', '').astype(float)

    # Display the first few rows of the dataframe
    df = pd.concat([df,df2,df3,df4,df5,df6,df7], axis=0)
    # Example usage during training
    df, vectorizer = preprocess_data(df)
    df = df.drop_duplicates(subset=['ASIN'])
    asinDf = df['ASIN']
    df = df.drop(['Product_Name','ASIN','Category'], axis =1)
    return df

def preprocess_reccomendation_data(df, vectorizer=None, fit_vectorizer=True):
    """
    Applies all transformations to the dataframe `df`.
    
    Args:
    - df: pandas DataFrame, input data to transform.
    - vectorizer: CountVectorizer instance, if None a new one will be created and fit.
    - fit_vectorizer: bool, whether to fit the CountVectorizer or not (useful at inference).
    
    Returns:
    - df: transformed pandas DataFrame.
    - vectorizer: fitted CountVectorizer instance.
    """
    
    # Fit and transform the product names
    if vectorizer is None:
        vectorizer = CountVectorizer(binary=True)
    
    if fit_vectorizer:
        X = vectorizer.fit_transform(df['Product Name']).toarray()
    else:
        X = vectorizer.transform(df['Product Name']).toarray()
    
    # Create a DataFrame with the one-hot encoded features
    df_one_hot = pd.DataFrame(X, columns=vectorizer.get_feature_names_out(), index=df.index)
    #df = df.drop(['Product Name'])
    # Concatenate the original DataFrame with the new one-hot encoded DataFrame
    df = pd.concat([df, df_one_hot], axis=1)
    df.fillna(0, inplace=True)
    df['Unit Count'] = df['Unit Count'].replace(0, 1)  # Replace 0 units with 1 to avoid division by zero
    df['true_price'] = df['Price'] / df['Unit Count']
    df['Keyword'] = df['Keyword'].replace({'men': 0, 'women': 1, 'missing': -1})  # Assuming 'missing' as -1 or another category
    
    # One-hot encode 'Category'
    one_hot_encoded = pd.get_dummies(df['Category'], prefix='Category')
    df = df.join(one_hot_encoded)
    
    # Replace spaces with underscores in column names and sort columns
    df.columns = [col.replace(' ', '_') for col in df.columns]
    df = df.sort_index(axis=1)
    
    return df, vectorizer
def reccomendedASINS(asin):
    original_index = 0

    # Preprocessing: Scale features (excluding 'true_price') for cosine similarity
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df)

    # Calculate cosine similarity
    cos_sim_matrix = cosine_similarity(scaled_features)

    # Extract similarity scores for the original row and create a DataFrame for them
    similarity_scores = pd.Series(cos_sim_matrix[original_index], index=df.index)

    # Add similarity scores to the original DataFrame (excluding the original row itself)
    df['similarity'] = similarity_scores
    df.reset_index(drop=True, inplace=True)
    df_filtered = df.drop(index=original_index)


    # Filter rows with lower 'true_price' and sort by similarity
    similar_rows = df_filtered[df_filtered['true_price'] < df.loc[original_index, 'true_price']].sort_values(by='similarity', ascending=False)

    # Select the top 3 most similar rows
    top_3_similar = similar_rows.head(3)

    return top_3_similar
