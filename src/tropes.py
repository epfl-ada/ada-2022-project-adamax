import pandas as pd
import helpers
import json
import string
import numpy as np
from collections import Counter
from scipy import stats
import helpers
import os


def normalize_title(m):
    m = m.lower().replace(" ", "").translate(str.maketrans('', '', string.punctuation))
    return m


def get_tvtropes_movies(path_to_json=None):
    # https://github.com/rhgarcia/tropescraper/raw/master/datasets/tvtropes_20200302.json.zip
    with open(path_to_json, "r") as f:
        movies_tropes_raw = json.load(f)
    movies_tvtropes = {}
    dupes = [] # drop all movies with duplicated normalized titles
    for k, v in movies_tropes_raw.items():
        k = normalize_title(k)
        if k not in movies_tvtropes:
            movies_tvtropes[k] = list(set([normalize_title(tr) for tr in v])) # avoid duplicated tropes
        else:
            dupes.append(k)
    for k in dupes:
        del movies_tvtropes[k]
    movie_titles = list(movies_tvtropes.keys())
    movie_tropes = list(movies_tvtropes.values())
    df = pd.DataFrame({"title": movie_titles, "trope": movie_tropes})
    return df


def merge_cmu_with_tvtropes(df_cmu, df_tvtropes):
    """Movies with duplicated titles are dropped
    """
    df_cmu = keep_movies_with_unique_titles(df_cmu)
    return pd.merge(df_cmu, df_tvtropes, on="title")


def keep_movies_with_unique_titles(df):
    df_new = df.assign(title=df["name"].apply(normalize_title))
    return df_new.loc[~df_new.duplicated(subset=["title"], keep=False)]


def add_bob_indicator(df):
    return df.assign(is_bomb_tvtropes=df["trope"].apply(lambda r: "boxofficebomb" in r))


if __name__ == "__main__":
    get_tvtropes_movies()