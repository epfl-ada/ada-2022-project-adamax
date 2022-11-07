### Helpers for the data processing
import pandas as pd
from collections import namedtuple

def get_characters():
    columns = ["WikiID", "FreebaseID", "ReleaseDate", "CharacterName", "ActorDOB", "ActorGender", "ActorHeight", "ActorEthnicity", "ActorName", "ActorAge", "FreebaseCharacterActorMapId", "FreebaseCharacterID", "FreebaseActorID"]
    return pd.read_csv('../data/character.metadata.tsv', sep='\t', names=columns, index_col=False)

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
    movies = pd.read_csv('../data/movie.metadata.tsv', sep='\t', names=columns, index_col=False)
    languages = movies["Language"]
    movies["Language"] = languages.apply(get_freebase_value)
    movies["LanguageID"] = languages.apply(get_freebase_id)

    countries = movies["Country"]
    movies["Country"] = countries.apply(get_freebase_value)
    movies["CountryID"] = countries.apply(get_freebase_id)

    genres = movies["Genres"]
    split_genres = genres.apply(lambda x: str.split(x, ','))
    movies["Genres"] = split_genres.apply(lambda x: [Genre(get_freebase_value(g), get_freebase_id(g)) for g in x])
    return movies

def get_plot_summaries():
    columns = ["WikiID", "Plot"]
    return pd.read_csv('../data/plot_summaries.txt', sep='\t', names=columns, index_col=False)