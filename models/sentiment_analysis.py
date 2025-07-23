import numpy as np
import pandas as pd
import joblib
import gensim
from gensim.models import Word2Vec
import gensim.downloader
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors


df = pd.read_csv("models/dataset.csv")
user_ratings = pd.read_csv("models/user_ratings.csv")
mlmodel = joblib.load("models/mlmodel")

## Pretrained embedding model
fasttext_300_wiki  = "fasttext-wiki-news-subwords-300"

class DataEmbeddings:
    def __init__(self, model_path=""):
        self.model = gensim.downloader.load(model_path)

    def get_model(self):
        return self.model

    def get_embeddings(self, reviews):
        tokens = [[word for sentence in sentences.split(".") for word in sentence.strip().split(" ") if sentence.strip() != "" if word in self.model.key_to_index] for sentences in reviews]
        return [self.model.get_mean_vector(token, pre_normalize=False) if token else np.zeros(self.model.vector_size) for token in tokens]

embed = DataEmbeddings(fasttext_300_wiki)


def getproducts(usrname):
    prod_index_list = []
    usr_id = df.loc[df['reviews_username'] == usrname.strip().lower(), 'reviews_username_label'].unique()[0]
    prod_ids = user_ratings.loc[usr_id-1].sort_values(ascending=False).index.astype("int")[:20].tolist()
    for prod_id in prod_ids:
        indices = df.loc[df["name_label"] == prod_id,:].sort_values(by="reviews_rating", ascending=False).index.tolist()
        eval_list = df.loc[indices, "reviews_text"].values.tolist()
        embed_vectors = embed.get_embeddings(eval_list)
        sentiment_list = mlmodel.predict(embed_vectors).tolist().index(1)
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
