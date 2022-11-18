#!/usr/bin/env python
# coding: utf-8

# In[18]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from helpers import *


# In[19]:


movies = get_movies()
movies.head()
genres = movies["genres"]


# We want to get a csv that relates all genres with the movies by having the genres as columns and movies as rows (if a movie is from a certain genre, said column will contain the value 1; otherwise, the value will be 0). For doing so, we need to extract all the genres and group the ones that are similar (for example: "Melodrama" is considered as just "Drama" ). 

# In[20]:


# First we get all the genres from the movies df without having repeated
genres = []
for g in movies.genres:
    for genre in g:
        if (genre not in genres and len(genre) > 0 and genre != "Film" ):
            genres.append(genre)

# Then, we get the genres that are only 1 word long, as they are the most general
genres_1word = []
for g in genres:
    if (len(g.split(" ")) == 1 and len(g.split("/")) == 1 and len(g.split("-")) == 1):
        genres_1word.append(g) 

print(len(genres))
print(len(genres_1word))


# In[21]:


# We check if the 1-word-genre is contained in longer genres ("Black comedy" will be considered as just "Comedy")
## If it is not, we add said genre in the array of 1-word-genres
for g in genres:
    notin = True
    for g1 in genres_1word:
        if g.lower().__contains__(g1.lower()):
            notin = False
    if notin:
        genres_1word.append(g) 

genres_1word.sort()
print(genres_1word)
print(len(genres_1word))


# In[22]:


for g in genres_1word:
    if (g.lower().__contains__("war")):
        print(g)


# We observed that there are still some genres that can be groupped, as they are pretty much the same or based on the same topic. Thus, we create a dictionary that gathers them in order to reduce the number of genres.

# In[23]:


dict_similar = {"Porn": ["Pornographic movie", "Pornography", "Softcore Porn"], 
                "LGBT": ["New Queer Cinema", "Gay", "Homoeroticism"],
                "Coming of age": ["Coming-of-age film"], "Erotica": ["Homoeroticism"], 
                "Comedy": ["Humour", "Tragicomedy", "Ealing Comedies", "Comdedy"], 
                "Language & Literature": ["& Literature"], 
                "Drama": ["Melodrama", "Tragedy", "Tragicomedy", "Docudrama"], 
                "Documentary": ["Political Documetary", "Docudrama", "Historical Documentaries", "Rockumentary"], 
                "Social issues": ["Social problem film"], 
                "War film": ["War effort", "The Netherlands in World War II", "Gulf War", "Combat Films"],
                "Alien Film": ["Alien invasion"],
                "Animation": ["Animated cartoon"],
                "Family & Personal Relationships": ["Family Film", "Interpersonal Relationship"],
                "Gross out": ["Gross-out Film"],
                "Dance": ["Hip hop movies", "Breakdance"],
                "History": ["Historical Documentaries"],
                "Political cinema": ["Political Documentary"],
                "Science Fiction": ["Sci Fi Picture original film"],
                "Buddy film": ["Buddy Picture", "Buddy cop"],
                "Music": ["Concert film", "Film-Opera", "Operetta", "Punk rock", "Rockumentary", "Space opera"], #Should we add Musical here?
                "Animals": ["Animal Picture"],
                "Religious Film": ["Christian film"],
                "Master Criminal Films": ["Heist", "Gangster Film"],
                "Film à clé": ["Film \\u00e0 clef"],
                "Biographical film": ["Biography", "Biopic [feature]"],
                "Beach Film": ["Beach Party film"],
                "World cinema": ["Chinese Movies", "Japanese Movies", "Latino", ""],
                "Musical": ["Singing cowboy"],
                "Western": ["Singing cowboy"]
            }


# In[24]:


# We add the key values of the dictionary (more general genres) and remove the genres contained in those general genres from the 1-word-genre array
for d in dict_similar:
    genres_1word.append(d)
    a = dict_similar[d]
    for dd in a:
        if (dd in genres_1word):
            genres_1word.remove(dd)

# To avoid having repeated values, we create a dictionary and then return to a list. We sort it so it is easier to read them.
main_genres = list(dict.fromkeys(genres_1word))
main_genres.sort()

print(main_genres)
print(len(main_genres))


# We create a function that will  allow us to determine wether a movie is from a genre or not

# In[31]:


def movie_has_genre(genresMovies, genre, dict_similar):
    """
    Check a genre given is contained in the genres from a movie, taken into account also the ones we have groupped into global genres
    Argument:
        genresMovies: it is a list with the genres of a film.
        genre: it is a string that represents a genre from the 1-word-genre array.
        dict_similar: it is a dictionary that has general-genres as keys and their similar genres (which can be classified under the general ones) as values.
    Returns:
        1 if the movies is from that genre (the genre passed is contained in the list of gentes of a film) or 0  otherwise.
    """
    array_genresMovies = genresMovies
    # We check if the genre is in the movie's genres
    for gm in array_genresMovies:
        if gm.lower().__contains__(genre.lower()):
            return 1
    # We also look in the genres we have grouped
    if (genre in dict_similar.keys()):
        for g in dict_similar[genre]:
            if g in array_genresMovies:
                return 1
    return 0
            


# In[37]:


# We create a df with the wiki_id, freebase_id, name and genres, and use the previous function to classify the movies into the different genres
movies_and_genres_df = movies[["wiki_id", "freebase_id", "name"]]

for genre in main_genres:
    movies_and_genres_df[genre] = movies["genres"].apply(lambda x: movie_has_genre(x, genre, dict_similar))


# In[38]:


print(len(movies_and_genres_df))
movies_and_genres_df.head()


# In[39]:


# We observe the distribution of movies according to the genres
## Count each genre column
count = movies_and_genres_df.loc[:,"Absurdism":].apply(lambda x: x.value_counts()).iloc[1]

count_genres = pd.DataFrame(count.items(), columns=["Genre", "Count"])

sns.set(rc={'figure.figsize':(20,8.27)})
ax = sns.barplot(x="Genre",y= "Count",  data=count_genres.sort_values(by="Count", ascending=False).head(15))


# Lastly, we get the csv we wanted from the df created

# In[40]:


# Save movies and genres to ../data/MovieSummaries/genres.csv
movies_and_genres_df.to_csv("../data/MovieSummaries/genres.csv")

