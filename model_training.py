# model_training.py

import pickle

import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


def train_content_based_model():
    site_df = pd.read_pickle("./pkl/preprocessed_site.pkl")

    site_df["text"] = (
        site_df["title"].fillna("")
        + " "
        + site_df["body"].fillna("")
        + " "
        + site_df["caption"].fillna("")
    )

    nltk.download("stopwords")
    stop_words = stopwords.words("portuguese")

    tfidf = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = tfidf.fit_transform(site_df["text"])

    nn_model = NearestNeighbors(metric="cosine", algorithm="brute")
    nn_model.fit(tfidf_matrix)

    with open("./pkl/tfidf.pkl", "wb") as f:
        pickle.dump(tfidf, f)
    with open("./pkl/nn_model.pkl", "wb") as f:
        pickle.dump(nn_model, f)
    site_df.to_pickle("./pkl/site_with_text.pkl")


if __name__ == "__main__":
    train_content_based_model()
