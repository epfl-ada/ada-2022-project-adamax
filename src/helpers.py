### Helpers for the data processing
import pandas as pd
import numpy as np
import cpi # For inflation adjusted revenue

movieSummariesPath = "../data/MovieSummaries"
imdbPath = "../data/Imdb"

### Import data from MovieSummaries
def get_characters():
    columns = ["wiki_id", "movie_freebase_id", "release_date", "character_name", "actor_dob", "actor_gender",
               "actor_height", "actor_ethnicity", "actor_name", "actor_age", "freebase_character_actor_map_id",
               "freebase_character_id", "freebase_actor_id"]
    return pd.read_csv(f'{movieSummariesPath}/character.metadata.tsv', sep='\t', names=columns, index_col=False)

def get_movies():
    columns = ["wiki_id", "freebase_id", "name", "release_date", "box_office_revenue", "runtime", "languages", "countries", "genres"]
    movies = pd.read_csv(f'{movieSummariesPath}/movie.metadata.tsv', sep='\t', names=columns, index_col=False)
    
    # Fix a mistake in the data
    movies.loc[movies["wiki_id"]==29666067, "release_date"] = "2010-12-02"
    movies["release_date"] = pd.to_datetime(movies["release_date"], errors='coerce')
    movies["year"] = movies["release_date"].apply(lambda x: x.year)
    movies["inflation_adjusted_revenue"] = movies.apply(
        lambda movie: cpi.inflate(movie["box_office_revenue"], int(movie["year"]), to=2021) if not np.isnan(movie["year"]) and movie["year"] >= 1913 else np.nan, axis=1)

    return movies

def get_plot_summaries():
    columns = ["wiki_id", "plot"]
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
    movies = pd.read_csv(f'{imdbPath}/movies_metadata.csv', index_col=False)
    movies["release_date"] = pd.to_datetime(movies["release_date"], errors='coerce')
    # Add a column for the year of release except for NaT values
    movies["year"] = movies["release_date"].apply(lambda x: x.year if not pd.isnull(x) else np.nan)
    movies["inflation_adjusted_revenue"] = movies.apply(
        lambda movie: cpi.inflate(int(movie["revenue"]), int(movie["year"]), to=2021) if not np.isnan(movie["year"]) and movie["year"] >= 1913 else np.nan, axis=1)
    movies["inflation_adjusted_budget"] = movies.apply(
        lambda movie: cpi.inflate(int(movie["budget"]), int(movie["year"]), to=2021) if not np.isnan(movie["year"]) and movie["year"] >= 1913 else np.nan, axis=1)
    return movies

def get_imdb_ratings_small():
    return pd.read_csv(f'{imdbPath}/ratings_small.csv', index_col=False)

def get_imdb_ratings():
    return pd.read_csv(f'{imdbPath}/ratings.csv', index_col=False)