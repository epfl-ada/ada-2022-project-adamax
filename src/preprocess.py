# import cpi  # For inflation adjusted revenue
import numpy as np
import pandas as pd

# cpi.update()
movieSummariesPath = "data/MovieSummaries"
imdbPath = "data/Imdb"


def adjust_to_inflation(revenue, year):

    if np.isnan(year) or year < 1913:
        return np.nan

    return cpi.inflate(int(revenue), int(year), to=2021)

# Add inflation adjusted revenue and budget columns to the MovieSummaries and the Imdb datasets


def preprocess():

    # Preprocess the MovieSummaries dataset
    movies = pd.read_csv(f'{movieSummariesPath}/movie.metadata.tsv', sep='\t', names=["wiki_id", "freebase_id",
                                                                                      "name", "release_date", "box_office_revenue", "runtime", "languages", "countries", "genres"], index_col=False)
    # Add inflation adjusted revenue column
    movies.loc[movies["wiki_id"] == 29666067, "release_date"] = "2010-12-02"
    movies["release_date"] = pd.to_datetime(movies["release_date"], errors='coerce')
    movies["year"] = movies["release_date"].apply(lambda x: x.year)
    movies["adj_revenue"] = movies.apply(lambda movie: cpi.inflate(movie["box_office_revenue"], int(movie["year"]), to=2021)
                                         if not np.isnan(movie["year"]) and movie["year"] >= 1913 else np.nan, axis=1)
    # Write to file
    movies.to_csv(f'{movieSummariesPath}/movie.metadata.csv')

    # Preprocess the Imdb dataset
    movies = pd.read_csv(f'{imdbPath}/movies_metadata.csv')
    # Add inflation adjusted revenue and budget columns
    movies["release_date"] = pd.to_datetime(movies["release_date"], errors='coerce')
    movies["year"] = movies["release_date"].apply(lambda x: x.year)
    movies["adj_revenue"] = movies.apply(lambda movie: adjust_to_inflation(movie["revenue"], movie["year"]), axis=1)
    movies["adj_budget"] = movies.apply(lambda movie: adjust_to_inflation(movie["budget"], movie["year"]), axis=1)
    movies["adj_profit"] = movies["adj_revenue"] - movies["adj_budget"]
    # Write to file
    movies.to_csv(f'{imdbPath}/movies_metadata.csv')


def compute_plot_embeddings():
    from sentence_transformers import SentenceTransformer
    from helpers import get_plot_summaries
    import pickle

    # nlp_model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')
    nlp_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

    plots_df = get_plot_summaries()
    sentences = plots_df["plot"].tolist()
    embeddings = nlp_model.encode(sentences, show_progress_bar=True, batch_size=128)
    print(embeddings.shape)

    embeddings_mapping = dict(zip(plots_df["wiki_id"].values, embeddings))
    with open("data/MovieSummaries/plots_embeddings_mpnet.pkl", "wb") as f:
        pickle.dump(embeddings_mapping, f)


compute_plot_embeddings()
