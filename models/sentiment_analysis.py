

import numpy as np
import pandas as pd
import joblib

df = pd.read_csv("dataset.csv")
user_ratings = pd.read_csv("user_ratings.csv")
mlmodel = joblib.load("mlmodel")
embed_vectors = np.load("embed_vectors.npy")

def getproducts(usrname):
    prod_index_list = []
    usr_id = df.loc[df['reviews_username'] == usrname.strip().lower(), 'reviews_username_label'].unique()[0]
    prod_ids = user_ratings.loc[usr_id-1].sort_values(ascending=False).index.astype("int")[:20].tolist()
    for prod_id in prod_ids:
        indices = df.loc[df["name_label"] == prod_id,:].sort_values(by="reviews_rating", ascending=False).index.tolist()
        sentiment_list = mlmodel.predict(embed_vectors[indices]).tolist().index(1)
        prod_index_list.append(indices[sentiment_list])
    prod_index_list = prod_index_list[:5]
    return df.loc[prod_index_list, :].reset_index(drop=True)

def get_product_list(usrname):
    prods_df = getproducts(usrname)
    products = [[prods_df.loc[ind, "name"], 
                {"id": f"{ind+1}", 
                 "ratings": prods_df.loc[ind, "reviews_rating"], 
                 "category":prods_df.loc[ind, "categories"], 
                 "manufacturer": prods_df.loc[ind, "manufacturer"], 
                 "brand": prods_df.loc[ind, "brand"], 
                 "userreview": prods_df.loc[ind, "reviews_text"]}] 
                for ind in range(5)]
    return products












