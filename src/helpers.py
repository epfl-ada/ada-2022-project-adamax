### Helpers for the data processing
import pandas as pd
# import cpi # For inflation adjusted revenue
from collections import namedtuple
import json
import xml.etree.ElementTree as ET
import gzip
import os
import shutil


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
    # movies["InflationAdjustedRevenue"] = movies.apply(
    #     lambda movie: cpi.inflate(movie["BoxOfficeRevenue"], int(movie["Year"]), to=2021) if not np.isnan(movie["Year"]) and movie["Year"] >= 1913 else np.nan, axis=1)

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

# Unzip all the .gz compressed data in ../data/corenlp_plot_summaries folder
# Assumes that the zipped files are present in the folder
def unzip_corenlp_plot_summaries():
    # Find all the .gz files in the data folder
    rootdir = '../data/corenlp_plot_summaries'
    gz_files = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith('.gz'):
                gz_files.append(os.path.join(subdir, file))

    # Unzip all the .gz files
    for gz_file in gz_files:
        with gzip.open(gz_file, 'rb') as f_in:
            with open(gz_file[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    # Remove all the .gz files
    for gz_file in gz_files:
        os.remove(gz_file)


def get_corenlp_father_words(count):
    # Father reference words
    father_reference_words = ["father", "dad", "papa"]

    # Store the count of father related words
    father_dependent_words = {}
    father_governor_words = {}

    # Parse and print out father information
    def get_father_info(root):
        for dep in root.iter('dep'):
            if dep.find("governor").text in father_reference_words:
                if dep.find("dependent").text in father_dependent_words:
                    father_dependent_words[dep.find("dependent").text] += 1
                else:
                    father_dependent_words[dep.find("dependent").text] = 1

            if dep.find("dependent").text in father_reference_words:
                if dep.find("governor").text in father_governor_words:
                    father_governor_words[dep.find("governor").text] += 1
                else:
                    father_governor_words[dep.find("governor").text] = 1
                
        
    # Find all the xml file names in the xmls directory
    rootdir = '../data/corenlp_plot_summaries'
    xml_files = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(subdir, file))

    x = 0
    # Parse each xml file (count for short circuiting)
    for xml_file in xml_files:
        if x > count:
            break
        x += 1
        tree = ET.parse(xml_file)
        root = tree.getroot()
        get_father_info(root)
        
    return father_dependent_words, father_governor_words