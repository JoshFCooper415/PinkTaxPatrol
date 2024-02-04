from sklearn.feature_extraction.text import CountVectorizer
import joblib  # for saving and loading sklearn models
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from lightgbm import LGBMClassifier
from sklearn.metrics.pairwise import cosine_similarity

# Function to apply all transformations
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
df = df.drop(['Product_Name','ASIN','Category'], axis =1)

original_index = 0

# Preprocessing: Scale features (excluding 'true_price') for cosine similarity
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[['feature1', 'feature2']])

# Calculate cosine similarity
cos_sim_matrix = cosine_similarity(scaled_features)

# Extract similarity scores for the original row and create a DataFrame for them
similarity_scores = pd.Series(cos_sim_matrix[original_index], index=df.index)

# Add similarity scores to the original DataFrame (excluding the original row itself)
df['similarity'] = similarity_scores
df_filtered = df.drop(index=original_index)

# Filter rows with lower 'true_price' and sort by similarity
similar_rows = df_filtered[df_filtered['true_price'] < df.loc[original_index, 'true_price']].sort_values(by='similarity', ascending=False)

# Select the top 3 most similar rows
top_3_similar = similar_rows.head(3)

print(top_3_similar)
