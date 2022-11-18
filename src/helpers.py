# Helpers for the data processing
import pandas as pd
import numpy as np
import json
from requests import get
from bs4 import BeautifulSoup
from collections import namedtuple

movieSummariesPath = "../data/MovieSummaries"
imdbPath = "../data/Imdb"

# Import data from MovieSummaries

Genre = namedtuple("Genre", ["name", "id"])


def get_characters():
    columns = ["wiki_id", "movie_freebase_id", "release_date", "character_name", "actor_dob", "actor_gender",
               "actor_height", "actor_ethnicity", "actor_name", "actor_age", "freebase_character_actor_map_id",
               "freebase_character_id", "freebase_actor_id"]
    return pd.read_csv(f'{movieSummariesPath}/character.metadata.tsv', sep='\t', names=columns, index_col=False)


def get_movies():
    # CMU dataset
    cmu_movies = pd.read_csv(f'{movieSummariesPath}/movie.metadata.csv', index_col=0)
    cmu_movies["genres"] = cmu_movies["genres"].apply(lambda x: json.loads(x))
    cmu_movies["genres"] = cmu_movies["genres"].apply(lambda x: set(x.values()))

    # IMDB dataset
    imdb_movies = pd.read_csv(f'{imdbPath}/movies_metadata.csv', index_col=0)
    imdb_movies["genres"] = imdb_movies["genres"].apply(lambda x: json.loads(x.replace("'", '"')))
    imdb_movies["genres"] = imdb_movies["genres"].apply(lambda x: set([e["name"] for e in x]))

    # ID pairs in order to memrge the dataset
    fbid_imdbid = pd.read_csv(f"{movieSummariesPath}/fbid_imdbdid_finally.csv", index_col=0)
    fbid_imdbid = fbid_imdbid.rename(columns={"FreebaseID": "freebase_id", "IMBD_ID": "imdb_id"})

    cmu_movies = cmu_movies.merge(fbid_imdbid, on="freebase_id")
    cmu_movies.dropna(subset=["imdb_id"], inplace=True)

    movies = cmu_movies.merge(imdb_movies, on=["imdb_id"])

    # Group the genres
    movies["genres"] = movies[["genres_x", "genres_y"]].apply(lambda x: x[0].union(x[1]), axis=1)
    movies = movies.drop(columns=["genres_x", "genres_y"])

    movies["year"] = movies["year_x"]
    movies = movies.drop(columns=["year_x", "year_y"])

    movies["release_date"] = movies["release_date_x"]
    movies = movies.drop(columns=["release_date_x", "release_date_y"])
    movies["release_date"] = pd.to_datetime(movies["release_date"])
    return movies


def get_plot_summaries():
    columns = ["wiki_id", "plot"]
    return pd.read_csv(f'{movieSummariesPath}/plot_summaries.txt', sep='\t', names=columns, index_col=False)

# Import data from Imdb


def get_imdb_credits():
    return pd.read_csv(f'{imdbPath}/credits.csv')


def get_imdb_keywords():
    return pd.read_csv(f'{imdbPath}/keywords.csv')


def get_imdb_links_small():
    return pd.read_csv(f'{imdbPath}/links_small.csv')


def get_imdb_links():
    return pd.read_csv(f'{imdbPath}/links.csv')


def get_imdb_movies():
    movies = pd.read_csv(f'{imdbPath}/movies_metadata.csv', index_col=0)


def get_imdb_ratings_small():
    return pd.read_csv(f'{imdbPath}/ratings_small.csv')


def get_imdb_ratings():
    return pd.read_csv(f'{imdbPath}/ratings.csv')


BOMBS_URL = "https://tvtropes.org/pmwiki/pmwiki.php/BoxOfficeBomb/"
SUB_URL = [
    "NumbersThroughB",
    "C",
    "D",
    "EThroughF",
    "GThroughH",
    "ItrhoughJ",
    "KtrhoughM",
    "NtrhoughR",
    "StrhoughT",
    "UtrhoughJ",
]


def get_bombs_title():
    titles = []
    for sub_url in SUB_URL:
        url = BOMBS_URL + sub_url
        r = get(url, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
        soup = BeautifulSoup(r.text)

        # get movie titles
        all_list = soup.find_all(name="li")
        for li in all_list:
            li = li.find("em")
            if li is None:
                continue
            li = li.find("a")
            if li is None:
                continue
            li = li.contents
            titles.append(li[0])
    return titles
