import pickle

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

with open("./pkl/tfidf.pkl", "rb") as f:
    tfidf = pickle.load(f)
with open("./pkl/nn_model.pkl", "rb") as f:
    nn_model = pickle.load(f)
site_df = pd.read_pickle("./pkl/site_with_text.pkl")
user_df = pd.read_pickle("./pkl/preprocessed_users.pkl")

indices = pd.Series(site_df.index, index=site_df["page"]).drop_duplicates()


def get_recommendations(user_history):
    idxs = [indices.get(page) for page in user_history if indices.get(page) is not None]

    if not idxs:
        recent_news = site_df.sort_values("Issued", ascending=False).head(10)
        return recent_news["page"].tolist()

    user_tfidf = tfidf.transform(site_df.loc[idxs]["text"])

    if user_tfidf.shape[0] == 1:
        user_profile = user_tfidf.toarray()
    else:
        user_profile = user_tfidf.mean(axis=0)
        user_profile = user_profile.A1
        user_profile = user_profile.reshape(1, -1)

    N_RECOMMENDATIONS = 100
    distances, indices_nn = nn_model.kneighbors(
        user_profile, n_neighbors=N_RECOMMENDATIONS
    )

    recommended = []
    for idx in indices_nn[0]:
        page_id = site_df.iloc[idx]["page"]
        if page_id not in user_history:
            issued_date = site_df.iloc[idx]["Issued"]
            recommended.append((page_id, issued_date))
        if len(recommended) >= 100:
            break

    recommended.sort(key=lambda x: x[1], reverse=True)

    final_recommendations = [rec[0] for rec in recommended[:10]]

    return final_recommendations


class RecommendationRequest(BaseModel):
    userId: str


@app.get("/recommend")
def recommend(userId: str):
    user = user_df[user_df["userId"] == userId]

    if user.empty:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user_history = user.iloc[0]["history"]
    recommendations = get_recommendations(user_history)

    return {"userId": userId, "recommendations": recommendations}
