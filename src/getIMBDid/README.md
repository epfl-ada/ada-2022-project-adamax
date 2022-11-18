# Get IMDB ids related to Freebase ids

### As we perform this action through requests to the Wiki Data webpage and our original dataset is 81k long, it takes around 20 hours. Thus, the requests are performed by 5 files, so the petitions are paralleled and the time is reduced to only 4 hours. These files are: `getmovies 1 copy1.ipynb`, `getmovies 1 copy2.ipynb`, `getmovies 1 copy3.ipynb`, `getmovies 1 copy4.ipynb` and `getmovies 1 copy5.ipynb`. 

### The other file in this folder is `create_csv_fbid_imbdid.ipynb`, which is used for creating a csv with the Freebase ids and IMDb ids related after all the requests have been perform.



