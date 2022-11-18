# The Big Flop

## Abstract

Producing a flop movie can be a disaster for a studio.
Unsuccessful productions, like Cleopatra (1963), have brought film production companies to the verge of bankruptcy.
In this project, our goal is to find the typical charecteristics of failing movies.

In order to do so, we need to define what consitutes a failing movie. 
We quantify the failure of a movie by two metrics: the profit and the general public's opinion.
We obtain these metrics from multiple datasets, such as the CMU Movie Summary Corpus, the IMDB dataset, and the TV Tropes Wiki.

Having quantified the failure, we are trying understand what factors, such as competition, character tropes or genre, contributing to a movies likelihood of failing. By conducting this investigation, we hope to provide guidance on how to avoid producing a movie that is likely to fail.

## Research questions

The research questions we want to answer with our analysis are:
1. What movies can be considered as failures?
2. Are there common characteristics between the failing movies?
3. Why does a movie fail and is it possible to avoid producing a failing movie?

## Proposed additional datasets

In addition to the provided CMU Movie Summary Corpus, we use the following additional datasets:

### [IMDb dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset).

This dataset is similar to our original dataset, but provides additional information about the user ratings, budget. production companies, etc. To merge this dataset with the original one, we scraped the IMDb id's related to the movies in our original dataset thus connecting the two datasets.

### [TV Tropes Wiki](https://tvtropes.org/pmwiki/pmwiki.php/Main/HomePage)

This webpage contains information about the tropes that appear in movies. We obtained a list with the trope information and joined the tropes with our original dataset by using the movie titles. For simplicity, we discarded the tropes their movie title matched multiple movie titles.

Additionally, the webpage provides a [list](https://tvtropes.org/pmwiki/pmwiki.php/Main/BoxOfficeBomb) of movies classified as 'Box Office Bombs'. We scraped this list and used it to define failing movies.

## Methods

### What movies can be considered as failures?

To filter the subset of failing movies from the dataset, we used three criteria:
- The movie's profit is negative in the IMDb data.
- The movie's rating is in the lowest quartile.
- The movie is classified as a 'Box Office Bomb' in the TV Tropes Wiki.

A movie's profit is calculated as the difference between the movie's budget and the movie's revenue. The profits are adjusted for inflation with U.S.
Consumer Price index using the [cpi python library](https://palewi.re/docs/cpi/). This adjustment is necessary to allow us to compare the magnitude of failure between movies produced in different years.

Using the profit calculated from the IMBd data is not necessarily a precise quantification of the movie's failure. The budget might not accurately represent the cost of producing the movie and additional costs such as marketing might not be included in the budget. Furthermore, the Box office revenue might not accurately represent the movie's profit for the studio because the revenue is divided by many parties, such as the theaters or distibution companies in addition to the studio. The revenue does not contain the total income genereated by the movie as it only takes into account the theter sales and thus omits profits generated from other sources, such as streaming or merchandise. Even though having a low profit is not a perfect metric for failure, we still assume that it can provide valuable information when deciding whether a movie is a failure.

We decided to use the lowest quartile of the ratings as a threshold for failure. We believe, that being in the lowest quartile of the ratings is a sufficient indicator of a movie's failure.

### Are there common characteristics between the failing movies?

After retrieving the failing movies, we will study if they are similar in terms of genre, trope analysis, competition, actors, budget and plot sentiment analysis. In future, we could also consider analyzing failing movies in different time periods.

In terms of genre, we wanted to find out which genres had the highest relative frequency of failing movies. We preprocessed the genres, reducing them to a set of 210 genres.

Image, analysis here



## Methods (this part should be the longest)
What counts as failing? Analyzing the bombs from TVTropes
Create three criteria : failing because of negative profit, bad review
Analyse the common points and differences among those criterions

Explore common characteristics of box-office bombs
Dividing the dataset into genres and time periods and compare success between them: use t-tests to compare revenue, budget, counts in each genre etc.
Use a pretrained language model to extract features from plots like sentiment analysis
Use a pretrained language model to encode plots and analyse the crowding distance of those plot embeddings.

Understand why some movies failed
    Competition effect:
See if the fact that another movie was released at the same time has an effect on being a bomb.
Using plot embeddings, study the same thing considering movies with a “similar” plot.
    Reaction from audience:
Sdf
Sdgsd
    Studio and Director history:
Sdgsfd
g

Does playing in a box-office bomb has a particular impact on an actor career?
Analyse some features in time, consider the release date of the bomb as a breaking point.


The budgets and revenues are adjusted for inflation using the [Consumer Price Index (CPI)](https://palewi.re/docs/cpi/)


Analyse new actor features (age of first appearance, frequency of acting, …) and establish a network of successful and failing actors (?)
Group the movies by tropes. We can cluster based on the semantic embeddings of the plot summaries (obtained with a pretrained language model). We can identify the tropes of a movie by comparing the embedding of the plot summary of the movie with the embedding of the description of the trope

## Data story (don’t see this part in the example projects the TA sent us)

## Proposed timeline

21 - 27/11:
28/11 - 4/12:  
5 - 11/12:
12 - 18/12:
19 - 23/12 (deadline):



## Done for Milestone 2
Merge IMDb dataset with CMF dataset
Scrape the budgets from wikipedia
Scrape the box office bombs from tvtropes.org
Scrape the tropes + initial analysis


TODO’s:
General statistics: revenues, budgets
Common genres?
Reasons of failure?
Ratings
Director
Box office bomb



















