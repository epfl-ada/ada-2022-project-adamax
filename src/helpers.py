### Helpers for the data processing
import pandas as pd
import numpy as np
from requests import get
from bs4 import BeautifulSoup

movieSummariesPath = "../data/MovieSummaries"
imdbPath = "../data/Imdb"

### Import data from MovieSummaries
def get_characters():
    columns = ["wiki_id", "movie_freebase_id", "release_date", "character_name", "actor_dob", "actor_gender",
               "actor_height", "actor_ethnicity", "actor_name", "actor_age", "freebase_character_actor_map_id",
               "freebase_character_id", "freebase_actor_id"]
    return pd.read_csv(f'{movieSummariesPath}/character.metadata.tsv', sep='\t', names=columns, index_col=False)

def get_movies():
    return pd.read_csv(f'{movieSummariesPath}/movie.metadata.csv')

def get_plot_summaries():
    columns = ["wiki_id", "plot"]
    return pd.read_csv(f'{movieSummariesPath}/plot_summaries.txt', sep='\t', names=columns, index_col=False)

### Import data from Imdb

def get_imdb_credits():
    return pd.read_csv(f'{imdbPath}/credits.csv')

def get_imdb_keywords():
    return pd.read_csv(f'{imdbPath}/keywords.csv')

def get_imdb_links_small():
    return pd.read_csv(f'{imdbPath}/links_small.csv')

def get_imdb_links():
    return pd.read_csv(f'{imdbPath}/links.csv')

def get_imdb_movies():
    return pd.read_csv(f'{imdbPath}/movies_metadata.csv')

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
        r = get(url)
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