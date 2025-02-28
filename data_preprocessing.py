import glob
import os

import pandas as pd


def preprocess_users(user_df):
    user_df["history"] = user_df["history"].apply(lambda x: x.strip('"').split(", "))
    user_df["timestampHistory"] = user_df["timestampHistory"].apply(
        lambda x: [int(ts) for ts in x.strip('"').split(", ")]
    )

    return user_df


def preprocess_site(site_df):
    site_df["Issued"] = pd.to_datetime(site_df["issued"])
    site_df["Modified"] = pd.to_datetime(site_df["modified"])

    return site_df


if __name__ == "__main__":
    site_files = glob.glob(os.path.join("./data/paginas", "*.csv"))
    site = pd.concat((pd.read_csv(f) for f in site_files), ignore_index=True)

    user_files = glob.glob(os.path.join("./data/users", "*.csv"))
    usuarios = pd.concat((pd.read_csv(f) for f in user_files), ignore_index=True)

    user_df = preprocess_users(usuarios)
    site_df = preprocess_site(site)

    user_df.to_pickle("./pkl/preprocessed_users.pkl")
    site_df.to_pickle("./pkl/preprocessed_site.pkl")
