# The Big Flop

The conducted analysis can be found on the notebook: `src/final_analysis.ipynb` and the data story from `antonpirhonen.github.io/ada-data-story`

## Abstract

In this project, we analyze low-rated movies and see what are their typical characteristics.
We obtain the movie data from two main sources: the CMU Movie Summary Corpus and the IMDB dataset.
During the project, we investigate how the factors, such as competition, movie topic and genre, contribute to a movie's rating.
By conducting this investigation, we hope to provide guidance on how to avoid producing a movie that is likely to receive bad reviews.

## Research questions

The research questions we want to answer with our analysis are:
1. Are there common characteristics between the failing movies?
2. Why does a movie fail and is it possible to predict which movie fails?

## Proposed additional datasets

In addition to the provided CMU Movie Summary Corpus, we use the following additional datasets:

### [IMDb dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)

This dataset is similar to our original dataset, but provides additional information about the movies, such as the user ratings, budget, production companies, keywords etc. To merge this dataset with the original one, we scraped the IMDb ids related to the movies in our original dataset thus connecting the two datasets.

## Methods

### Researching common characteristics between the failing movies

For the purposes of this analysis, we defined a low rated movie (a failure) as a movie having an user rating less than 5.5/10.
We study if they are similar in terms of genre, budget, revenue, competition and keywords.
We use both regression and classification methods to answer the research questions.
Regression methods are used to predict the user rating of a movie based on the features we are interested in, whereas classification methods are used to predict whether a movie is a failure or not.

### Outlook on the features

**Genre**
In terms of genre, we analyzed which genres had the lowest rating. The following violin plot shows the worst rated genres. We used genre as a one-hot encoded variable for the regression analysis.

<p align="center">
  <img src="img/bottom_10_genres.png" style="width: 600px;"/>
</p>

**Competition**
To analyse the effect of competition on being a low rated movie, we studied the causal effect of the number of movies released each week, month or year optionally grouped by genres. We trained a linear model to predict if a movie is a failure based on those features and in addition to features like budget, vote_average, popularity. 

**Keywords**
Keywords are a good indicator of the movie topic. We cluster the keywords into topics by considering the list of keywords for each movie as a text document, and then use Latent Dirichlet Allocation (LDA) for topic modelling. Then, we use the most probable topic of a movie to predict its rating.

## Results
 - Classification performed better than regression, but both methods are still unlikely to be able to accurately predict movie ratings.
 - Nevertheless, extracted features are useful to understand general characteristics of failing movies, from both the general analysis and the attempts to predict movie ratings.

## Team organization
| Member   |      Tasks      |
|----------|:-------------:|
| Everybody | Writing the data story |
| Ana | Data processing, general analysis, genre analysis <br> Hosting the data story website |
| Anton | Data processing, general analysis <br> Working on the data story website | 
| Hédi | General analysis, descriptive analysis <br> finding features, regression analysis, actor analysis |
| Son | Regression and classification analysis <br> keyword analysis, trying out different models |

## Reference