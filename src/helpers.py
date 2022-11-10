### Helpers for the data processing
import numpy as np
import pandas as pd
import cpi
from collections import namedtuple

movieSummariesPath = "../data/MovieSummaries"
imdbPath = "../data/Imdb"

### Import data from MovieSummaries
def get_characters():
    columns = ["WikiID", "MovieID", "ReleaseDate", "CharacterName", "ActorDOB", "ActorGender", "ActorHeight", "ActorEthnicity", "ActorName", "ActorAge", "FreebaseCharacterActorMapId", "FreebaseCharacterID", "FreebaseActorID"]
    return pd.read_csv(f'{movieSummariesPath}/character.metadata.tsv', sep='\t', names=columns, index_col=False)

def get_freebase_value(s):
    l = str.split(s, ':')
    if len(l) <= 1:
        return ""
    l = l[1]
    for c in [ "\"", "}", "Language" ]:
        l = l.replace(c, "")
    return l.strip()

def get_freebase_id(s):
    l = str.split(s, ':')
    if len(l) <= 1:
        return ""
    l = l[0]
    for c in [ "\"", "{"]:
        l = l.replace(c, "")
    return l.strip()

Genre = namedtuple("Genre", ["name", "id"])

def get_movies():
    columns = ["WikiID", "FreebaseID", "Name", "ReleaseDate", "BoxOfficeRevenue", "Runtime", "Language", "Country", "Genres"]
    movies = pd.read_csv(f'{movieSummariesPath}/movie.metadata.tsv', sep='\t', names=columns, index_col=False)
    languages = movies["Language"]
    movies["Language"] = languages.apply(get_freebase_value)
    movies["LanguageID"] = languages.apply(get_freebase_id)

    countries = movies["Country"]
    movies["Country"] = countries.apply(get_freebase_value)
    movies["CountryID"] = countries.apply(get_freebase_id)

    genres = movies["Genres"]
    split_genres = genres.apply(lambda x: str.split(x, ','))
    movies["Genres"] = split_genres.apply(lambda x: [Genre(get_freebase_value(g), get_freebase_id(g)) for g in x])

    movies["ReleaseDate"] = pd.to_datetime(movies["ReleaseDate"])
    movies["Year"] = movies["ReleaseDate"].apply(lambda x: x.year)
    movies["InflationAdjustedRevenue"] = movies.apply(
        lambda movie: cpi.inflate(movie["BoxOfficeRevenue"], int(movie["Year"]), to=2021) if not np.isnan(movie["Year"]) and movie["Year"] >= 1913 else np.nan, axis=1)

    return movies

def get_plot_summaries():
    columns = ["WikiID", "Plot"]
    return pd.read_csv(f'{movieSummariesPath}/plot_summaries.txt', sep='\t', names=columns, index_col=False)

### Import data from Imdb

def get_imdb_credits():
    return pd.read_csv(f'{imdbPath}/credits.csv', index_col=False)

def get_imdb_keywords():
    return pd.read_csv(f'{imdbPath}/keywords.csv', index_col=False)

def get_imdb_links_small():
    return pd.read_csv(f'{imdbPath}/links_small.csv', index_col=False)

def get_imdb_links():
    return pd.read_csv(f'{imdbPath}/links.csv', index_col=False)

def get_imdb_movies():
    return pd.read_csv(f'{imdbPath}/movies_metadata.csv', index_col=False)

def get_imdb_ratings_small():
    return pd.read_csv(f'{imdbPath}/ratings_small.csv', index_col=False)

def get_imdb_ratings():
    return pd.read_csv(f'{imdbPath}/ratings.csv', index_col=False)